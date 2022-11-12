import logging

import requests
import json
from .celery import app
from django.conf import settings
from celery.utils.log import get_task_logger
from datetime import datetime

from main.models import Message

logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)

@app.task(bind=True)
def send_message(self, message_id, minuts_retry_sending):
    message = Message.objects.get(pk=message_id)
    message_phone = message.client.phone_number
    message_text = message.mail_list.text
    data_json = json.loads(f'{{"id": "{message_id}", "phone": "{message_phone}", "text": "{message_text}"}}')
    message.datetime_sending = datetime.now() # для обновления значения в случае неотправки
    message.save()
    try:
        requests.post(url=settings.URL_SERVICE_SEND_MESSAGE+str(message.pk),
                      headers=settings.AUTH_HEADERS, json=data_json)
    except requests.exceptions.RequestException as exc:
        logger.info(f'Sending message with id: {message_id} failed, repeat sending in {minuts_retry_sending}')
        message.status_sending = 0 # статус: ошибка при отправке
        message.save()
        self.retry(exc=exc, countdown=minuts_retry_sending*60)
    else:
        logger.info(f'Message with id: {message_id} has been sent')
        message.status_sending = 1 # статус: отправлено
        message.save()



