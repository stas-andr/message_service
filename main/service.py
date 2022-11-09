import pytz
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from message_service.tasks import send_message

from .models import MailList, Client, GroupClients, Message

timezone = pytz.timezone(settings.TIME_ZONE)


def create_messages(mail_list, clients, sending_datetime):
    """
    create and send messages for clients in mail_list in sending_datetime
    """
    for client in clients:
        message = Message(client=client, datetime_sending=datetime.now(), mail_list=mail_list)
        send_message.apply_async((message.pk, mail_list.interval_minutes_failed_message), eta=sending_datetime)

def post_save_maillist(sender, instance: MailList, created,  **kwargs):
    print("post_save_maillist")
    if created:
        filter = instance.filter
        try:
            mobile_operators = filter["mobile_operators"]
        except KeyError:
            mobile_operators = []
        try:
            tags = filter["tags"]
        except KeyError:
            tags = []
        clients = Client.objects.filter(Q(tag__tag__in=tags) | Q(mobile_operator__name__in=mobile_operators))
        datetime_now = timezone.localize(datetime.now())
        if datetime_now <= instance.datetime_stop and datetime_now >= instance.datetime_start:
            # отправить сообщения из рассылки
            print("отправить сообщение из рассылки")
            create_messages(instance, clients, datetime_now)
        elif datetime_now < instance.datetime_start:
            # отложить отправление сообщения
            print("отложить отправление сообщения")
            create_messages(instance, clients, instance.datetime_start)