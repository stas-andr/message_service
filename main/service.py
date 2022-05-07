from datetime import datetime

def post_save_maillist(sender, instance, created,  **kwargs):
    if created:
        if datetime.now() <= instance.datetime_stop and datetime.now() >= instance.datetime_stop:
            # отправить сообщения из рассылки
            pass
        elif datetime.now() < instance.datetime_start:
            # отложить отправление сообщения
            pass