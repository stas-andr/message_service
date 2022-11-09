from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from main.models import Client, MailList
from .serializers import ClientSerializer, MailListSerializer


@api_view(['GET'])
def clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def mail_lists(request):
    if request.method == 'GET':
        mail_lists = MailList.objects.all()
        serializer = MailListSerializer(mail_lists, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def mail_list_detail(request, pk, format=None):
    if request.method == 'GET':
        try:
            mail_list = MailList.objects.get (pk=pk)
        except MailList.DoesNotExist:
            return Response (status=status.HTTP_404_NOT_FOUND)
        serializer = MailListSerializer(mail_list)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MailListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

