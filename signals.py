from django.db.models.signals import post_save
from django.dispatch import receiver
    
from .apps import AuthentaConfig as conf
from .models import Task

@receiver(post_save, sender=Task)
def StartingTask(sender, instance, created, **kwargs):
    if created:
        instance.prepare()
        instance.can_run()
    else:
        if instance.status == conf.Task.status_ready:
            instance.start_task()