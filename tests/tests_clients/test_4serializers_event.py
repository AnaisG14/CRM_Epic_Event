import pytest
import copy
from datetime import datetime
from authentication.models import User
from clients.models import Client, Contract, Event
from clients.serializers import EventDetailSerializer


class TestEventSerializer:

    @classmethod
    def setup(cls):
        cls.sailor = User.objects.create_user(username='Sailor1', role='Sailor team')
        cls.supporter = User.objects.create_user(username='Supporter1',
                                                 role='Support team')
        cls.client = Client.objects.create(first_name='John',
                                           last_name='Doe',
                                           email='johndoe@test.com',
                                           phone='00632562',
                                           mobile='036479536',
                                           company_name='Doe Enterprise',
                                           sales_contact=cls.sailor)
        cls.contract = Contract.objects.create(sales_contact=cls.sailor,
                                               client=cls.client,
                                               status=1,
                                               amount=100.00,
                                               payment_due=datetime.now())

        cls.serializer = EventDetailSerializer
        event_date = datetime.now()

        cls.valid_data = {'contract': cls.contract.pk,
                          'client': cls.client.pk,
                          'support_contact': cls.supporter.pk,
                          'event_status': 'IN PROGRESS',
                          'attendees': 50,
                          'event_date': event_date,
                          'notes': 'birthday'
                          }

    @pytest.mark.django_db
    def test_valid_serializer(self):
        serializer = self.serializer(data=self.valid_data)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_serializer_missing_required_field(self):
        """Test if all required fields are ok"""

        # missing support_contact
        data_without_support_contact = copy.deepcopy(self.valid_data)
        del data_without_support_contact['support_contact']
        serializer = self.serializer(data=data_without_support_contact)
        assert not serializer.is_valid()
        assert serializer.errors['support_contact']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing contract
        data_without_contract = copy.deepcopy(self.valid_data)
        del data_without_contract['contract']
        serializer = self.serializer(data=data_without_contract)
        assert not serializer.is_valid()
        assert serializer.errors['contract']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing event_status
        data_without_event_status = copy.deepcopy(self.valid_data)
        del data_without_event_status['event_status']
        serializer = self.serializer(data=data_without_event_status)
        assert not serializer.is_valid()
        assert serializer.errors['event_status']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing attendees
        data_without_attendees = copy.deepcopy(self.valid_data)
        del data_without_attendees['attendees']
        serializer = self.serializer(data=data_without_attendees)
        assert not serializer.is_valid()
        assert serializer.errors['attendees']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing event_date
        data_without_event_date = copy.deepcopy(self.valid_data)
        del data_without_event_date['event_date']
        serializer = self.serializer(data=data_without_event_date)
        assert not serializer.is_valid()
        assert serializer.errors['event_date']
        assert serializer.error_messages['required'] == 'This field is required.'

    @pytest.mark.django_db
    def test_invalid_field(self):
        """Test if all required fields are ok"""
        # event status is a valid choice
        data_event_status = copy.deepcopy(self.valid_data)
        del data_event_status['event_status']
        data_event_status['event_status'] = 'bad choice'
        serializer = self.serializer(data=data_event_status)
        assert not serializer.is_valid()
        assert serializer.errors['event_status']

        # attendees is an integer
        data_attendees_is_int = copy.deepcopy(self.valid_data)
        del data_attendees_is_int['attendees']
        data_attendees_is_int['attendees'] = 'number'
        serializer = self.serializer(data=data_attendees_is_int)
        assert not serializer.is_valid()
        assert serializer.errors['attendees']
