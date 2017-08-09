from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .apps import AuthentaConfig, logmethis

if AuthentaConfig.mail_activation:
    @receiver(post_save, sender=User)
    def sendMail_UserCreate(sender, instance, created, **kwargs):
        if created:
            instance.sendMail()