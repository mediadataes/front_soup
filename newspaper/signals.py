import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Newspaper


def get_or_create_schedule(hour, minute='00'):
    schedule, _ = CrontabSchedule.objects.get_or_create(minute=minute,
                                                        hour=hour,
                                                        timezone=settings.TIME_ZONE)
    return schedule


@receiver(post_save, sender=Newspaper, dispatch_uid=None)
def post_save_handler(sender, instance, created,**kwargs):
    for time in ['morning', 'afternoon', 'night']:
        obj_time = getattr(instance, time)
        strtime = obj_time.strftime('%H.%M')
        task_name = '{} {}'.format(instance.name, time)
        schedule = get_or_create_schedule(obj_time.hour, obj_time.minute)
        if created and instance.active:
            task = PeriodicTask.objects.create(
                crontab=schedule,
                name=task_name,
                task='data.tasks.download_url',
                args= json.dumps([instance.pk, strtime, instance.url])
            )
        elif not created and instance.active:
            defaults = {
                'name': task_name,
                'crontab': schedule,
                'task': 'data.tasks.download_url',
                'args': json.dumps([instance.pk, strtime, instance.url])
            }
            task = PeriodicTask.objects.update_or_create(name=task_name,
                                                         defaults=defaults)
        elif not created and not instance.active:
            PeriodicTask.objects.get(name=task_name).delete()


@receiver(post_delete, sender=Newspaper, dispatch_uid=None)
def post_delete_handler(sender, instance, **kwargs):
    for time in ['morning', 'afternoon', 'night']:
        obj_time = getattr(instance, time)
        task_name = '{} {}'.format(instance.name, time)
        if instance.active:
            PeriodicTask.objects.get(name=task_name).delete()
