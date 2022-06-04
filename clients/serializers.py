from rest_framework.serializers import ModelSerializer, ValidationError
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
        read_only_fields = ['client']


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
        read_only_fields = ['client']


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
            'event',
        ]
        read_only_fields = ['event', 'sales_contact']


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
        read_only_fields = ['event', 'sales_contact']


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
            'status',
            'contracts_client'
        ]
        read_only_fields = ['contracts_client', 'sales_contact']

    def validate(self, data):
        # Check that the client is not already in the database
        if Client.objects.filter(email=data['email'], last_name=data['last_name']).exists():
            raise ValidationError('Client already exists.')
        return data


class ClientDetailSerializer(ModelSerializer):

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
                  'status',
                  'contracts_client',
                  ]
        read_only_fields = ['contracts_client']
