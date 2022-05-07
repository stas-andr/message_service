from .celery import app


@app.task
def send_message(id, phone, text):
    pass