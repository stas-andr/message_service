from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from jsonschema import validate
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError


SCHEMA_FILTER_JSON = {
    'type': 'object',
    'schema': 'http://json-schema.org/draft-07/schema#',
    'properties': {
        'tags': {'type': 'array'},
        'mobile_operators': {'type': 'array'}
    },
    'anyOf': [
        {'required': ['tags']},
        {'required': ['mobile_operator']}
    ]
}


class JSONSchemaValidator(BaseValidator):
    def compare(self, a, b):
        try:
            result = validate(a, b)
        except Exception as e:
            raise ValidationError(e)
        else:
            return result


class MailList(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    datetime_stop = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    filter = models.JSONField(validators=[JSONSchemaValidator(limit_value=SCHEMA_FILTER_JSON)])
    # если сообщение не отправилось, повторить через interval_minutes_failed_message, по дефолту 1 сутки
    interval_minutes_failed_message = models.IntegerField(default=24*60,
        verbose_name='Через сколько минут повторить неудачную отправку')

    def __str__(self):
        return f'{self.text}, начинается {self.datetime_start}, кончается {self.datetime_stop}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = "Рассылки"


class GroupClients(models.Model):
    tag = models.CharField(max_length=32, verbose_name='Тег (произвольная метка)')
    name = models.CharField(max_length=32, verbose_name='Имя группы пользователей')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Группа клиентов'
        verbose_name_plural = "Группы клиентов"


class MobileOperator(models.Model):
    code_regex = RegexValidator(regex = r'^\d{2,3}$')
    code = models.CharField(max_length=3, validators=[code_regex])
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Мобильный оператор'
        verbose_name_plural = "Мобильные операторы"


class Client(models.Model):
    phone_number_regex = RegexValidator(regex = r'^7\d{10}$')
    phone_number = models.CharField(validators=[phone_number_regex], max_length=11, unique=True, null=False)
    mobile_operator = models.ForeignKey(MobileOperator, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(GroupClients, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32, choices=settings.TIMEZONES,
                                default='UTC')

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    STATUSES_SENDING = (
        (1, "Отправлено"),
        (0, "Ошибка при отправке"),
        (2, "Создано")
    )
    datetime_sending = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status_sending = models.IntegerField(choices=STATUSES_SENDING, verbose_name='Статус отправки', default=2)
    mail_list = models.ForeignKey(MailList, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")

    def __str__(self):
        return f'Рассылка: {self.mail_list}, дата отправки: {self.datetime_sending}, клиент: {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = "Сообщения"


