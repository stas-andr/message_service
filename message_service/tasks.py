from .celery import app
from django.conf import settings

@app.task(bind=True)
def send_message(self, id, phone, text):
    print(settings.auth_headers)
    pass