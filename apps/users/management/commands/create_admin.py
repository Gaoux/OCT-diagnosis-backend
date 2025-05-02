from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un usuario administrador por defecto si no existe'

    def handle(self, *args, **kwargs):
        email = "admin@example.com"
        password = "admin123"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                name="Admin Default",
                role="admin" , 
                is_verified=True
            )
            self.stdout.write(self.style.SUCCESS(' Superusuario creado correctamente'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe'))
