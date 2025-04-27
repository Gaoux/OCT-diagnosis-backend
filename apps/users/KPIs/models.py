from django.db import models
from django.utils.timezone import now
from apps.users.models import UserAccount


class ErrorReport(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='error_reports')
    description = models.TextField()  # Descripción del error
    created_at = models.DateTimeField(default=now)  # Fecha en que se reportó el error
    resolved = models.BooleanField(default=False)  # Si el error ha sido resuelto

    def __str__(self):
        return f"Error reportado por {self.user.email} - Resuelto: {self.resolved}"