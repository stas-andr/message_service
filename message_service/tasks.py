import requests
from .celery import app
from django.conf import settings

@app.task(bind=True)
def send_message(self, id, phone, text):
    requests.post(settings.URL_SERVICE_SEND_MESSAGE, headers=settings.AUTH_HEADERS,
                  )

