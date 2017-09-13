from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from .apps import AuthentaConfig, logmethis

UserModel = get_user_model()

if AuthentaConfig.mail_activation:
    @receiver(post_save, sender=UserModel)
    def sendMail_UserCreate(sender, instance, created, **kwargs):
        if created:
            instance.sendMail()