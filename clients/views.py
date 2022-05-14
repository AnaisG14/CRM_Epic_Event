from rest_framework.viewsets import ModelViewSet
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer


class ClientAPIViewSet(ModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.all()


class ContractAPIViewSet(ModelViewSet):
    
    serializer_class = ContractSerializer
    
    def get_queryset(self):
        return Contract.objects.all()


class EventAPIViewSet(ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()
