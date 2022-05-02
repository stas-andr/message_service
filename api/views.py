from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Client
from .serializers import ClientSerializer

@api_view(['GET', 'POST'])
def clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


