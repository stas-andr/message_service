from django.views import generic
from rest_framework import generics
from rest_framework import views

from main.models import Client, MailList, Message
from .serializers import ClientSerializer, MailListSerializer, MessageSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailListView(generics.ListCreateAPIView):
    queryset = MailList.objects.all()
    serializer_class = MailListSerializer


class MailListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MailList.objects.all()
    serializer_class = MailListSerializer


class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

