import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_service.settings')
app = Celery('message_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()