from django.db import models
from django.utils.timezone import now
from apps.users.models import CustomUser

class ErrorReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='error_reports')
    description = models.TextField()  # Descripción del error
    created_at = models.DateTimeField(default=now)  # Fecha en que se reportó el error
    resolved = models.BooleanField(default=False)  # Si el error ha sido resuelto
    level = models.CharField(max_length=50, default='ERROR')  # Nivel del error (INFO, WARNING, ERROR)

    def __str__(self):
        return f"Error reportado por {self.user.email} - Resuelto: {self.resolved}"