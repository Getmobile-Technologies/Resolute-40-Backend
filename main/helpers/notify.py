from main.models import Notifications

def notification_handler(organisation, message):
    notifier = Notifications.objects.create(organisation=organisation, message=message)

    return notifier