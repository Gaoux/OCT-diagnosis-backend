import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Ensure email is provided and normalize it
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        role = extra_fields.pop('role', 'patient')
        if role not in ['patient', 'professional', 'admin']:
           role = 'patient'  # fallback seguro
        
        # Create user without a username (since you are using email)
        user = self.model(email=email,role=role, **extra_fields)
        
        # Set the password
        user.set_password(password)
        
        # Save the user instance to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="UUID generado automáticamente"
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    login_count = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    ROLES = [
        ('patient', 'Patient'),
        ('professional', 'Professional'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='patient')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    class Meta:
        db_table = 'user_account'
        verbose_name = 'User account'
        verbose_name_plural = 'User accounts'

    def __str__(self):
        return self.email

