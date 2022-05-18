from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer,\
    ContractDetailSerializer, ContractListSerializer,\
    EventListSerializer, EventDetailSerializer
from .permissions import IsAuthorizedToAccessClient


class ClientAPIViewSet(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessClient]

    # self.request.object.contract.event.support_contact.pk

    def get_queryset(self):
        clients = Client.objects.all()
        if self.request.user.role == "SUPPORT":
            events = Event.objects.filter(support_contact=self.request.user)
            clients_supporter = []
            for event in events:
                # for instance in event:
                if event.support_contact == self.request.user:
                    clients_supporter.append(event.client.pk)
            return Client.objects.filter(id__in=clients_supporter)
        return clients

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class ContractAPIViewSet(ModelViewSet):
    
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        contracts = Contract.objects.all()
        client_id = self.request.GET.get('client_id')
        if client_id is not None:
            contracts = contracts.filter(client=client_id)
        return contracts

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class EventAPIViewSet(ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()
