from rest_framework.serializers import ModelSerializer
from .models import Client, Contract, Event


class EventListSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'contract',
            'date_created',
            'date_updated',
            'client',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes',
        ]


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'contract',
            'date_created',
            'date_updated',
            'client',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes',
        ]


class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = [
            'pk',
            'sales_contact',
            'client',
            'date_created',
            'date_updated',
            'status',
            'amount',
            'payment_due',
            'event'
        ]


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = [
            'pk',
            'sales_contact',
            'client',
            'date_created',
            'date_updated',
            'status',
            'amount',
            'payment_due',
            'event'
        ]


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'sales_contact',
        ]


class ClientDetailSerializer(ModelSerializer):

    contracts_client = ContractListSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'company_name',
                  'date_created',
                  'date_updated',
                  'sales_contact',
                  'contracts_client',
                  ]
