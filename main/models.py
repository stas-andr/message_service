from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class MailList(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    datetime_stop = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    filter = models.JSONField()

    def __str__(self):
        return f'{self.text}, начинается {self.datetime_start}, кончается {self.datetime_stop}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = "Рассылки"


class MobileOperator(models.Model):
    code_regex = RegexValidator(regex = r'^\d{2,3}$')
    code = models.CharField(max_length=3, validators=[code_regex], null=False, verbose_name="Код мобильного оператора")
    name = models.CharField(max_length=32, verbose_name="Имя мобильного оператора")

    def __str__(self):
        return f'{self.name} c кодом: {self.code}'

    class Meta:
        verbose_name = 'Мобильный оператор'
        verbose_name_plural = "Мобильные операторы"


class GroupClients(models.Model):
    tag = models.CharField(max_length=32, verbose_name='Тег (произвольная метка)', null=False)
    name = models.CharField(max_length=32, verbose_name='Имя группы пользователей')

    def __str__(self):
        return f'{self.name} с тегом: {self.tag}'

    class Meta:
        verbose_name = 'Группа клиентов'
        verbose_name_plural = "Группы клиентов"


class Client(models.Model):
    phone_number_regex = RegexValidator(regex = r'^7\d{10}$')
    phone_number = models.CharField(validators=[phone_number_regex], max_length=11, unique=True, null=False)
    mobile_operator = models.ForeignKey(MobileOperator, on_delete=models.DO_NOTHING, verbose_name='Код мобильного оператора'),
    group_clients = models.ForeignKey(GroupClients, on_delete=models.CASCADE),
    timezone = models.CharField(max_length=32, choices=settings.TIMEZONES,
                                default='UTC')

    def __str__(self):
        return f'Номер телефона: {self.phone_number}, мобильный оператор: {self.mobile_operator}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    STATUSES_SENDING = (
        (1, "Sent"),
        (0, "Not sent"),
    )
    datetime_sending = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status_sending = models.IntegerField(choices=STATUSES_SENDING, verbose_name='Статус отправки', default=0)
    mail_list = models.ForeignKey(MailList, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рассылка: {self.mail_list}, дата отправки: {self.datetime_sending}, клиент: {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = "Сообщения"

