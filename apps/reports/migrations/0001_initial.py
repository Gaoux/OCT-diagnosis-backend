# Generated by Django 5.2 on 2025-05-12 00:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('file_path', models.CharField(max_length=500)),
                ('file_format', models.CharField(max_length=10)),
                ('file_size_kb', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('predicted_diagnostic', models.CharField(max_length=100)),
                ('diagnostic_probabilities', models.JSONField()),
                ('comments', models.TextField(blank=True)),
                ('patient_name', models.CharField(blank=True, max_length=100)),
                ('document_id', models.CharField(blank=True, max_length=50)),
                ('eye_side', models.CharField(blank=True, choices=[('OD', 'OD (Right Eye)'), ('OS', 'OS (Left Eye)')], default='OD', max_length=2)),
                ('visual_acuity', models.CharField(blank=True, max_length=20)),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reports.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
