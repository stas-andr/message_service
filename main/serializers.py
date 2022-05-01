from rest_framework.serializers import ModelSerializer
from .models import Message, Client, MobileOperator, MailList, GroupClients


class MailListSerializer(ModelSerializer):
    class Meta:
        model = MailList
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MobileOperatorSerializer(ModelSerializer):
    class Meta:
        model = MobileOperator
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class GroupClientsSerializer(ModelSerializer):
    class Meta:
        model = GroupClients
        fields = "__all__"
