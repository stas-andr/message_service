from django.db import models

class MailList(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    datetime_stop = models.DateTimeField(verbose_name='Дата и время окончания рассылки')

class Client(model.Model):


