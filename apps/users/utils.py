from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
import os

def send_verification_email(user, request):
    token = AccessToken.for_user(user) 
    verify_link = f"{settings.FRONTEND_URL}/verify-email?token={str(token)}"

    subject = "Confirma tu cuenta"
    text_content = f"Hola {user.name}, confirma tu cuenta aquí: {verify_link}"

    html_content = f"""
    <html>
      <body>
        <h2>¡Hola {user.name}!</h2>
        <p>Gracias por registrarte. Por favor confirma tu cuenta haciendo clic en el siguiente enlace:</p>
        <a href="{verify_link}" style="padding:10px 20px; background-color:blue; color:white; text-decoration:none;">Confirmar Cuenta</a>
        <p>Si no solicitaste este correo, puedes ignorarlo.</p>
      </body>
    </html>
    """

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_reset_password_email(user, request):
    token = AccessToken.for_user(user)  
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={str(token)}"

    subject = "Restablece tu contraseña"
    text_content = f"Hola {user.name}, restablece tu contraseña aquí: {reset_link}"

    html_content = f"""
    <html>
      <body>
        <h2>¡Hola {user.name}!</h2>
        <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente botón:</p>
        <a href="{reset_link}" style="padding:10px 20px; background-color:green; color:white; text-decoration:none;">Restablecer Contraseña</a>
        <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
      </body>
    </html>
    """

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
