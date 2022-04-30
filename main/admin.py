from django.contrib import admin
from main.models import Client, Message, MailList, GroupClients, MobileOperator

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(MailList)
admin.site.register(GroupClients)
admin.site.register(MobileOperator)
