from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'profession']
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
        fields = ['id', 'email', 'name', 'profession', 'is_admin']
