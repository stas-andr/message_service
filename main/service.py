from datetime import datetime
from django.db.models import Q
from message_service.tasks import send_message

from .models import MailList, Client, GroupClients

def post_save_maillist(sender, instance:MailList, created,  **kwargs):
    print("post_save_maillist")
    if created:
        filter = instance.filter
        mobile_operators = filter["mobile_operators"]
        tags = filter["tags"]
        clients = Client.objects.filter(Q(tag__name__in=tags) | Q(mobile_operator__name__in=mobile_operators))
        if datetime.now() <= instance.datetime_stop and datetime.now() >= instance.datetime_stop:
            # отправить сообщения из рассылки
            pass
        elif datetime.now() < instance.datetime_start:
            # отложить отправление сообщения
            pass