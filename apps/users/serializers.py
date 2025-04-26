from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Ese email ya está registrado.")
        return value

    def create(self, validated_data): 
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'role', 'is_admin')

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para ver detalles completos de un usuario"""
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'role', 'is_admin', 'date_joined')
        read_only_fields = ('date_joined',)

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios desde el panel de administración"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'role', 'is_admin')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'currentPassword', 'newPassword', 'confirmPassword')
        extra_kwargs = {
            'email': {'required': False},
            'name': {'required': False}
        }
    
    def validate(self, data):
        # Validación solo si se envía nueva contraseña
        if 'newPassword' in data and data['newPassword']:
            if 'currentPassword' not in data or not data['current_password']:
                raise serializers.ValidationError({"current_password": "Current password is required"})
            
            if not self.instance.check_password(data['currentPassword']):
                raise serializers.ValidationError({"currentPassword": "Incorrect password"})
        
        return data
    
    def update(self, instance, validated_data):
        # Actualizar contraseña
        if 'newPassword' in validated_data and validated_data['newPassword']:
            instance.set_password(validated_data.pop('newPassword'))
            validated_data.pop('currentPassword', None)
        
        # Actualizar otros campos
        return super().update(instance, validated_data)

class AdminRegistrationSerializer(serializers.ModelSerializer):
    """Serializer específico para crear administradores"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
    
    def create(self, validated_data):
        validated_data['role'] = 'admin'
        validated_data['is_admin'] = True
        return CustomUser.objects.create_user(**validated_data)

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para las estadísticas del dashboard"""
    total_users = serializers.IntegerField()
    total_patients = serializers.IntegerField()
    total_ophthalmologists = serializers.IntegerField()
    total_admins = serializers.IntegerField()
    
class RecentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'date_joined']