from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Ensure email is provided and normalize it
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Create user without a username (since you are using email)
        user = self.model(email=email, **extra_fields)
        
        # Set the password
        user.set_password(password)
        
        # Save the user instance to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    login_count = models.PositiveIntegerField(default=0)  # Nuevo campo para contar inicios de sesión

    # Use email as the unique identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    # Use the custom user manager
    objects = CustomUserManager()

    ROLES = [
        ('normal', 'Normal'),
        ('professional', 'Professional'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='normal')

    def __str__(self):
        return self.username

