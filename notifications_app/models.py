from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create your models here.


class BroadcastNotification(models.Model):
    message = models.CharField(max_length=100)
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']


@receiver(post_save, sender=BroadcastNotification)
def broadcast_after_save(sender, instance, created, **kwargs):
    print("inside broadcast_after_save")
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=instance.broadcast_on.hour, minute=instance.broadcast_on.minute, day_of_month=instance.broadcast_on.day, month_of_year=instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(
            instance.id), task='notifications_app.tasks.broadcast_notifications', args=json.dumps((instance.id,)))
        print("task scheduled")
