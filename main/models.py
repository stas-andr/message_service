from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class MailList(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    datetime_stop = models.DateTimeField(verbose_name='Дата и время окончания рассылки')

class Client(models.Model):
    phoneNumberRegex = RegexValidator(regex = r'^7\d{10}$')
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=11, unique=True, null=False)
    codeOperator = models.CharField(max_length=3, null=False)
    tag = models.CharField(max_length=32)
    timezone = models.CharField(max_length=32, choices=settings.TIMEZONES,
                                default='UTC')

class Message(models.Model):
    datetime_sending = models.DateTimeField(verbose_name='Дата отправки')
    status_sending = models.IntegerField(verbose_name='Статус отправки')
    id_maillist = models.ForeignKey(MailList, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

