from celery import Celery

app = Celery('message_service', broker='redis://10.17.0.140:6379')

if __name__ == '__main__':
    app.start()