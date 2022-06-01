import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer,\
    ContractDetailSerializer, ContractListSerializer,\
    EventListSerializer, EventDetailSerializer
from .permissions import IsAuthorizedToAccessClientOrContract, IsAuthorizedSailorOrAssignedSupporterToManageEvents


class ClientAPIViewSet(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessClientOrContract]
    filter_backends = [SearchFilter]
    search_fields = ['last_name', 'sales_contact__username', 'status']

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
        if self.action == 'retrieve' or self.action == 'update':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class ContractAPIViewSet(ModelViewSet):
    
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessClientOrContract]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'sales_contact__username', 'status']
    ordering_fields = ['payment_due']

    def get_queryset(self):
        contracts = Contract.objects.all()
        if self.request.user.role == "SUPPORT":
            events = Event.objects.filter(support_contact=self.request.user)
            contracts_supporter = [event.contract.pk for event in events]
            return Contract.objects.filter(id__in=contracts_supporter)
        return contracts

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class EventAPIViewSet(ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedSailorOrAssignedSupporterToManageEvents]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'support_contact__username']
    ordering_fields = ['event_date']

    def get_queryset(self):
        events = Event.objects.all()
        if self.request.user.role == 'SUPPORT':
            return Event.objects.filter(support_contact=self.request.user.id)
        return events

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        contract_id = request.data['contract']
        contract = Contract.objects.get(pk=contract_id)
        client = Client.objects.get(pk=contract.client.id)
        request.data["client"] = client.pk
        request.POST._mutable = False
        return super().create(request, *args, **kwargs)

