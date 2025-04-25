import uuid
from django.db import models
from apps.users.models import CustomUser

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(upload_to='uploads/', null=True, blank=True)
    file_path = models.CharField(max_length=500)
    file_format = models.CharField(max_length=10)
    file_size_kb = models.IntegerField()

    def __str__(self):
        return f"{self.file_path} ({self.file_format})"

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    predicted_diagnostic = models.CharField(max_length=100)
    diagnostic_probabilities = models.JSONField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Report of {self.user.name} - {self.predicted_diagnostic}"
