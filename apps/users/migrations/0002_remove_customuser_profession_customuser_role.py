# Generated by Django 4.2.20 on 2025-04-12 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profession',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('paciente', 'Paciente'), ('oftalmologo', 'Oftalmólogo'), ('admin', 'Administrador')], default='paciente', max_length=20),
        ),
    ]
