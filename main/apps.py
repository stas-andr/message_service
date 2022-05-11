from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Сервис для рассылки'

    def ready(self):
        from .service import post_save_maillist
        from django.db.models.signals import post_save
        from .models import MailList

        post_save.connect(post_save_maillist, sender=MailList)
