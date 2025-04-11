from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    ROLES = [
        ('paciente', 'Paciente'),
        ('oftalmologo', 'Oftalmólogo'),
        ('admin', 'Administrador'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='paciente')

    def __str__(self):
        return self.username