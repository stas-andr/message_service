import pytz
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from message_service.tasks import send_message

from .models import MailList, Client, GroupClients

timezone = pytz.timezone(settings.TIME_ZONE)


def post_save_maillist(sender, instance:MailList, created,  **kwargs):
    print("post_save_maillist")
    if created:
        filter = instance.filter
        mobile_operators = []
        tags = []
        try:
            mobile_operators = filter["mobile_operators"]
            tags = filter["tags"]
        except KeyError:
            # одно из полей точно заполнено
            pass
        clients = Client.objects.filter(Q(tag__name__in=tags) | Q(mobile_operator__name__in=mobile_operators))
        datetime_now = timezone.localize(datetime.now())
        if datetime_now <= instance.datetime_stop and datetime_now >= instance.datetime_start:
            # отправить сообщения из рассылки
            print("отправить сообщение из рассылки")
        elif datetime_now < instance.datetime_start:
            # отложить отправление сообщения
            print("отложить отправление сообщения")