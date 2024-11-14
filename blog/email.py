from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def envoyer_email(prenom, nom, email, adresse, message):
    # Email pour l'équipe interne
    sujet_interne = "Nouvelle demande de contact"
    message_html_interne = render_to_string('email.html', {
        'prenom': prenom,
        'nom': nom,
        'email': email,
        'adresse': adresse,
        'message': message
    })
    message_texte_interne = strip_tags(message_html_interne)
    destinataires_interne = [settings.EMAIL_HOST_USER]

    # Envoyer l'email à l'équipe interne
    send_mail(
        sujet_interne,
        message_texte_interne,
        settings.EMAIL_HOST_USER,
        destinataires_interne,
        fail_silently=False,
        html_message=message_html_interne,
    )

    # Email de confirmation pour l'utilisateur
    sujet_confirmation = "Confirmation de votre demande de contact"
    message_html_confirmation = render_to_string('email_confirmation.html', {
        'prenom': prenom,
        'nom': nom
    })
    message_texte_confirmation = strip_tags(message_html_confirmation)

    # Envoyer l'email de confirmation à l'utilisateur
    send_mail(
        sujet_confirmation,
        message_texte_confirmation,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=message_html_confirmation,
    )
