from django.contrib import admin
from main.models import Client, Message, MailList, GroupClients, MobileOperator

class ClientAdmin(admin.ModelAdmin):
    pass
    # list_display = ('phone_number', 'mobile_operator','timezone')


admin.site.register(MobileOperator)
admin.site.register(GroupClients)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message)
admin.site.register(MailList)


