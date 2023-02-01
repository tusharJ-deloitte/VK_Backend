from celery import shared_task
from .models import BroadcastNotification
from celery import states, Celery
from celery.exceptions import Ignore
import asyncio
from channels.layers import get_channel_layer
import json


@shared_task(bind=True)
def broadcast_notifications(self, notification_id):
    print("data => "+notification_id)
    try:
        notifications = BroadcastNotification.objects.filter(
            id=int(notification_id))
        if len(notifications) > 0:
            print(notifications)
            notification = notifications.first()
            channel_layer = get_channel_layer()
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    "type": "send_notification",
                    "message": json.dumps(notification.message),
                }))
            notification.sent = True
            notification.save()
            return "notification sent"
        else:
            print("Notification not found")
            self.update_state(
                state="FAILURE",
                meta={
                    "exe": "Not Found"
                }
            )
            raise Ignore()
    except:
        print("Notification not found")
        self.update_state(
            state="FAILURE",
            meta={
                "exe": "Not Found"
            }
        )
    return 'Done'
