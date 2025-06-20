from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .utils import send_verification_email, send_reset_password_email
from .filters import UserFilter
from .permissions import IsAdminUser

from .models import UserAccount
from .serializers import AdminRegistrationSerializer, AdminUserUpdateSerializer, DashboardStatsSerializer, RegisterSerializer, UserCreateSerializer, UserDetailSerializer, UserSerializer, RecentUserSerializer, UserUpdateSerializer
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = False
            user.save()
            send_verification_email(user, request)
            return Response({'message': 'Usuario creado, revisa tu correo para verificar'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            if not user.is_verified:
                return Response({'error': 'Debes confirmar tu correo antes de iniciar sesión.'}, status=status.HTTP_403_FORBIDDEN)

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

class AdminUserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        print(">>>> PATCH data received:", data)  # DEBUG HERE
        # Handle password update
        new_password = data.get('password')
        if new_password:
            user.set_password(new_password)
            user.save()
            data.pop('password', None)  # Avoid issues with serializer

        serializer = AdminUserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario actualizado correctamente', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Ahora las vistas para el CRUD y el dashboard
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD completo de usuarios.
    Solo accesible para administradores.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserAccount.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email', 'name']  # Permite buscar por email y nombre
    filterset_class = UserFilter  # Usa el filtro personalizado para 'role'

    # permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        """
        Selecciona el serializer adecuado según la acción.
        """
        if self.action == 'list':
            return UserSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AdminUserUpdateSerializer
        return UserDetailSerializer

    def get_queryset(self):
        """
        Personaliza el queryset para incluir filtros de búsqueda.
        """
        queryset = UserAccount.objects.all()
        search = self.request.query_params.get('search', None)

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(name__icontains=search)
            )

        return queryset

class AdminRegistrationView(APIView):
    """
    Vista para registrar específicamente administradores.
    """
   # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Administrador registrado correctamente'}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(APIView):
    """
    Vista para obtener estadísticas del dashboard.
    Solo accesible para administradores.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        stats = {
            'total_users': UserAccount.objects.count(),
            'total_patients': UserAccount.objects.filter(role='patient').count(),
            'total_ophthalmologists': UserAccount.objects.filter(role='professional').count(),
            'total_admins': UserAccount.objects.filter(role='admin').count(),
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
    #permission_classes = [IsAdminUser]

    def get(self, request):
        # Obtén los últimos 5 usuarios registrados
        recent_users = UserAccount.objects.order_by('-date_joined')[:5]
        serializer = RecentUserSerializer(recent_users, many=True)
        return Response(serializer.data)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        print("TOKEN RECIBIDO:", token)
        try:
            access_token = AccessToken(token)
            print("TOKEN DECODIFICADO:", access_token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response({'message': 'Correo verificado exitosamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Token error:", str(e))  
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                return Response({'error': 'Correo no verificado'}, status=status.HTTP_400_BAD_REQUEST)
            send_reset_password_email(user, request)
            return Response({'message': 'Correo de restablecimiento enviado'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Correo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('password')

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Token error:", str(e))
            return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

