from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BroadcastNotification
from .tasks import broadcast_notifications

# Create your views here.


def home(request):
    return render(request, 'app1/base.html', {'room_name': 'broadcast'})


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            "type": "send_notification",
            "message": ["Notification1", "Notification2", "Notification3"]
        }
    )
    # notification = BroadcastNotification()
    # notification.message = "Event Registered Successfully"
    # notification.broadcast_on = date
    return HttpResponse("Done")

def test_celery(request):
    print('request received')
    broadcast_notifications.delay()
    return HttpResponse("Done")
