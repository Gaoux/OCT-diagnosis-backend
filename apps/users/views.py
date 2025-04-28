from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, RecentUserSerializer
from .models import UserAccount
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            user.login_count += 1
            user.save()

            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            })
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id',  'email', 'name', 'role', 'is_admin', 'date_joined')
        read_only_fields = ('date_joined',)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserAccount
        fields = ('id',  'email', 'password', 'name', 'role', 'is_admin')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserAccount.objects.create_user(
            password=password,
            **validated_data
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'name', 'role', 'is_admin')

class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'password', 'name')
    
    def create(self, validated_data):
        validated_data['role'] = 'admin'
        password = validated_data.pop('password')
        user = UserAccount.objects.create_user(
            password=password,
            **validated_data
        )
        return user

class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_patients = serializers.IntegerField()
    total_ophthalmologists = serializers.IntegerField()
    total_admins = serializers.IntegerField()

# Permiso personalizado para administradores
class IsAdminUser(IsAuthenticated):
    """Permiso personalizado que verifica si el usuario es administrador"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'

# Ahora las vistas para el CRUD y el dashboard
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD completo de usuarios.
    Solo accesible para administradores.
    """
    queryset = UserAccount.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [ 'email', 'name']
    filterset_fields = ['role']
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def get_queryset(self):
        queryset = UserAccount.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) | 
                Q(name__icontains=search)
            )
        return queryset

class RegisterAdminView(APIView):
    """
    Vista para registrar administradores.
    """
    permission_classes = [IsAdminUser]  

    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Administrador registrado correctamente'}, status=status.HTTP_201_CREATED)

class DashboardStatsView(APIView):
    """
    Vista para obtener estadísticas del dashboard.
    Solo accesible para administradores.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        stats = {
            'total_users': CustomUser.objects.count(),
            'total_patients': CustomUser.objects.filter(role='normal').count(),
            'total_ophthalmologists': CustomUser.objects.filter(role='professional').count(),
            'total_admins': CustomUser.objects.filter(role='admin').count(),
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True  # ← Esto permite actualización parcial
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(
            {"detail": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
class RecentUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Obtén los últimos 5 usuarios registrados
        recent_users = CustomUser.objects.order_by('-date_joined')[:5]
        serializer = RecentUserSerializer(recent_users, many=True)
        return Response(serializer.data)