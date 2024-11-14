# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Blog, Newsletter

@receiver(post_save, sender=Blog)  # Remplacez BlogPost par le modèle de votre article
def notify_subscribers_on_new_post(sender, instance, created, **kwargs):
    if created:  # Seulement lors de la création d'un nouvel article
        subscribers = Newsletter.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]
        
        send_mail(
            subject="Nouvel article publié : " + instance.title,
            message=f"Un nouvel article a été publié : {instance.title}\n\n{instance.content}",
            from_email="votre_email@example.com",
            recipient_list=recipient_list,
        )
