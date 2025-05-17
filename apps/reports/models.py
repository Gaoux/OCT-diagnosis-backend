import uuid
from django.db import models
from apps.users.models import UserAccount

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
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    predicted_diagnostic = models.CharField(max_length=100)
    diagnostic_probabilities = models.JSONField()
    comments = models.TextField(blank=True)

    patient_name = models.CharField(max_length=100, blank=True) 
    document_id = models.CharField(max_length=50, blank=True) 

    EYE_CHOICES = [
        ('OD', 'OD (Right Eye)'),
        ('OS', 'OS (Left Eye)'),
    ]
    eye_side = models.CharField(max_length=2, choices=EYE_CHOICES, default='OD', blank=True)  # OD/OS

    visual_acuity = models.CharField(max_length=20, blank=True)  # Agudeza visual (can be formatted like 20/20 or 6/6)

    def __str__(self):
        return f"Report of {self.user.name} - {self.predicted_diagnostic}"
