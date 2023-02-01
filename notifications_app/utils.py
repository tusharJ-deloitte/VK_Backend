from .models import BroadcastNotification
from datetime import datetime, timedelta


def schedule_notification_task(event_name, start_time):
    try:
        # after creation of event
        message = f"New Event {event_name} created. Go and Register now."
        time = datetime.now() + timedelta(minutes=2)
        notification = BroadcastNotification(
            message=message, broadcast_on=time)
        notification.save()

        # 1 hr before start time
        time = start_time - timedelta(hours=1)
        if datetime.now() < time :
            message = f"{event_name} will be starting in 1 hr, Be Ready. If not registered, Register Now."
            notification = BroadcastNotification(
                message=message, broadcast_on=time)
            notification.save()

        # 10 minutes before start time
        time = start_time - timedelta(minutes=10)
        if datetime.now() < time:
            message = f"{event_name} will be starting in 10 minutes, Be Ready. If not registered, Register Now."
            notification = BroadcastNotification(
                message=message, broadcast_on=time)
            notification.save()

        # 5 mintues before start time
        time = start_time - timedelta(minutes=5)
        if datetime.now() < time:
            message = f"{event_name} will be starting in 5 minutes, Be Ready. If not registered, Register Now."
            notification = BroadcastNotification(
                message=message, broadcast_on=time)
            notification.save()

    except:
        return "Error Occured"
