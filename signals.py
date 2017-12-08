from django.db.models.signals import post_save
from django.dispatch import receiver
    
from .apps import AuthentaConfig as conf
from .models import Task, Method

@receiver(post_save, sender=Task)
def TaskStarting(sender, instance, created, **kwargs):
    if created:
        instance.prepare()
        instance.can_run()
    else:
        if instance.status == conf.Task.status_ready:
            instance.start_task()

@receiver(post_save, sender=Method)
def MethodCaching(sender, instance, created, **kwargs):
    task = Task(task='cache_methods', status='order', info='From signal')
    task.save()