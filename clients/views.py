from rest_framework.viewsets import ModelViewSet
from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer,\
    ContractDetailSerializer, ContractListSerializer,\
    EventListSerializer, EventDetailSerializer


class ClientAPIViewSet(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class ContractAPIViewSet(ModelViewSet):
    
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    
    def get_queryset(self):
        return Contract.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class EventAPIViewSet(ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()
