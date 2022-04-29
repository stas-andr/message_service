from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class MailList(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    datetime_stop = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

class GroupClients(models.Model):
    tag = models.CharField(max_length=32, verbose_name='Тег (произвольная метка)', null=False)

class Client(models.Model):
    phone_number_regex = RegexValidator(regex = r'^7\d{10}$')
    phone_number = models.CharField(validators=[phone_number_regex], max_length=11, unique=True, null=False)
    code_operator = models.CharField(max_length=3, null=False)
    tag = models.ForeignKey(GroupClients, on_delete=models.SET_DEFAULT, default=None)
    timezone = models.CharField(max_length=32, choices=settings.TIMEZONES,
                                default='UTC')

class Message(models.Model):
    datetime_sending = models.DateTimeField(verbose_name='Дата отправки')
    status_sending = models.IntegerField(verbose_name='Статус отправки')
    id_maillist = models.ForeignKey(MailList, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Filter(models.Model):
    name = models.CharField(max_length=32, null=True)

class MobileOperator(models.Model):
    code_regex = RegexValidator(regex = r'^\d{2,3}$')
    code = models.CharField(max_length="3", validators=[code_regex], null=False)

class FilterCodeOperator(models.Model):
    filter = models.ForeignKey(Filter, null=False)
    code_operator = models.ForeignKey()

