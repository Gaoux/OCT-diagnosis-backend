from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.template.loader import render_to_string

def send_verification_email(user, request):
    token = AccessToken.for_user(user) 
    verify_link = f"{settings.FRONTEND_URL}/verify-email?token={str(token)}"

    subject = "OCTSENSE: Confirma tu cuenta"
    text_content = f"""
    Hola {user.name},
    
    Gracias por registrarte en OCTSENSE. Por favor confirma tu cuenta en este enlace: {verify_link}
    
    Si no solicitaste este correo, puedes ignorarlo.
    
    Saludos,
    El equipo de OCTSENSE
    """

    html_content = render_to_string("emails/verify_email.html", {
        "user": user,
        "verify_link": verify_link,
        "FRONTEND_URL": settings.FRONTEND_URL,
    })

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_reset_password_email(user, request):
    token = AccessToken.for_user(user)  
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={str(token)}"

    subject = "OCTSENSE: Restablece tu contraseña"
    text_content = f"Hola {user.name}, has solicitado restablecer tu contraseña. Usa este enlace: {reset_link}"

    html_content = render_to_string("emails/reset_password.html", {
        "user": user,
        "reset_link": reset_link,
        "FRONTEND_URL": settings.FRONTEND_URL,
    })

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
