import requests
import json
from .celery import app
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True)
def send_message(self, message, minuts_retry_sending):
    message_id = str(message.pk)
    message_phone = message.client.phone_number
    message_text = message.mail_list.text
    data_json = json.loads(f'{{"id": {message_id}, "phone": {message_phone}, "text": {message_text}}}')
    try:
        requests.post(url=settings.URL_SERVICE_SEND_MESSAGE+str(message.pk),
                      headers=settings.AUTH_HEADERS, json=data_json)
    except requests.exceptions.RequestException as exc:
        logger.info(f'Sending message with id: {message_id} failed, repeat sending in {minuts_retry_sending}')
        message.status_sending = 0 # статус: ошибка при отправке
        self.retry(exc=exc)
    else:
        logger.info(f'Message with id: {message_id} has been sent')
        message.status_sending = 1 # статус: отправлено



