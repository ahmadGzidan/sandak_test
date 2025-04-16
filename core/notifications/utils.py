from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def create_notification(user, title, message):
    notif = Notification.objects.create(user=user, title=title, message=message)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send.notification",
            "data": {
                "title": notif.title,
                "message": notif.message,
                "created_at": notif.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        }
    )
