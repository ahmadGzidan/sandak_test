from celery import shared_task
from notifications.utils import create_notification
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_medicine_reminder(user_id, med_name):
    try:
        user = User.objects.get(id=user_id)
        create_notification(user, "Medicine Reminder", f"Time to take {med_name}")
    except User.DoesNotExist:
        pass
