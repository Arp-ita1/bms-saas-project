from .models import Notification


def create_notification(title, message, user=None, customer=None):
    return Notification.objects.create(title=title, message=message, user=user, customer=customer)
