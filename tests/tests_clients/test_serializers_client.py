import pytest
import copy
import datetime
from authentication.models import User
from clients.models import Client, Contract, Event
from clients.serializers import ClientSerializer


class TestClientSerializer:

    @classmethod
    def setup(cls):
        cls.sailor = User.objects.create_user(username='Sailor1',
                                              role='Sailor team')
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
                                               payment_due=datetime.datetime.now())
        cls.event = Event.objects.create(support_contact=cls.supporter,
                                         event_status='In progress',
                                         attendees=50,
                                         event_date=datetime.datetime.now(),
                                         notes="birthday",
                                         contract=cls.contract,
                                         client=cls.client,
                                         )

        cls.serializer = ClientSerializer
        
        contracts_client = {
            'pk': cls.contract.pk,
            'sales_contact': cls.sailor.pk,
            'client': cls.client.pk,
            'date_created': cls.format_datetime(cls.contract.date_created),
            'date_updated': cls.format_datetime(cls.contract.date_updated),
            'status': True,
            'amount': '100.00',
            'payment_due': cls.format_datetime(cls.contract.payment_due),
            'event': cls.event.pk
        }
        
        cls.valid_data = {'first_name': 'John',
                          'last_name': 'Doe',
                          'email': 'johndoe@test.com',
                          'phone': '00632562',
                          'mobile': '036479536',
                          'company_name': 'Doe Enterprise',
                          'sales_contact': cls.sailor.id,
                          'contracts_client': [contracts_client]
                          }

    @classmethod
    def format_datetime(cls, value):
        """ Return a type datetime in string"""
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @pytest.mark.django_db
    def test_valid_serializer(self):
        serializer = self.serializer(data=self.valid_data)
        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_serializer_missing_required_field(self):
        """Test if all required fields are ok"""
        # missing first_name
        data_without_first_name = copy.deepcopy(self.valid_data)
        del data_without_first_name['first_name']
        serializer = self.serializer(data=data_without_first_name)
        assert not serializer.is_valid()
        assert serializer.errors['first_name']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing last_name
        data_without_last_name = copy.deepcopy(self.valid_data)
        del data_without_last_name['last_name']
        serializer = self.serializer(data=data_without_last_name)
        assert not serializer.is_valid()
        assert serializer.errors['last_name']
        assert serializer.error_messages['required'] == 'This field is required.'
        
        # missing email
        data_without_email = copy.deepcopy(self.valid_data)
        del data_without_email['email']
        serializer = self.serializer(data=data_without_email)
        assert not serializer.is_valid()
        assert serializer.errors['email']
        assert serializer.error_messages['required'] == 'This field is required.'

        # # missing phone not required
        # data_without_phone = copy.deepcopy(self.valid_data)
        # del data_without_phone['phone']
        # serializer = self.serializer(data=data_without_phone)
        # data_without_phone['phone'] = ''
        # assert serializer.is_valid()
        # assert not serializer.errors['phone']

        # missing mobile
        data_without_mobile = copy.deepcopy(self.valid_data)
        del data_without_mobile['mobile']
        serializer = self.serializer(data=data_without_mobile)
        assert not serializer.is_valid()
        assert serializer.errors['mobile']
        assert serializer.error_messages['required'] == 'This field is required.'

        # missing sales_contact
        data_without_sales_contact = copy.deepcopy(self.valid_data)
        del data_without_sales_contact['sales_contact']
        serializer = self.serializer(data=data_without_sales_contact)
        assert not serializer.is_valid()
        assert serializer.errors['sales_contact']
        assert serializer.error_messages['required'] == 'This field is required.'

    @pytest.mark.django_db
    def test_invalid_field(self):
        """Test if required fields are valid"""
        # length of first_name and last_name
        data_with_too_long_first_name = copy.deepcopy(self.valid_data)
        del data_with_too_long_first_name['first_name']
        data_with_too_long_first_name['first_name']= 'a_first_name_very_very_very_long'
        serializer = self.serializer(data=data_with_too_long_first_name)
        assert not serializer.is_valid()
        assert serializer.errors['first_name']
        # assert serializer.error_messages['max_length'] == 'Ensure this field has no more than 25 characters.'

        data_with_too_long_last_name = copy.deepcopy(self.valid_data)
        del data_with_too_long_last_name['last_name']
        data_with_too_long_last_name['last_name'] = 'a_last_name_very_very_very_long'
        serializer = self.serializer(data=data_with_too_long_last_name)
        assert not serializer.is_valid()
        assert serializer.errors['last_name']

        # length phone and mobile
        data_with_too_long_phone = copy.deepcopy(self.valid_data)
        del data_with_too_long_phone['phone']
        data_with_too_long_phone['phone'] = 'a_phone_name_very_very_very_long'
        serializer = self.serializer(data=data_with_too_long_phone)
        assert not serializer.is_valid()
        assert serializer.errors['phone']

        data_with_too_long_mobile = copy.deepcopy(self.valid_data)
        del data_with_too_long_mobile['mobile']
        data_with_too_long_mobile['mobile'] = 'a_mobile_name_very_very_very_long'
        serializer = self.serializer(data=data_with_too_long_mobile)
        assert not serializer.is_valid()
        assert serializer.errors['mobile']

    @pytest.mark.django_db
    def test_invalid_datatype_sales_contact(self):
        data_with_invalid_sales_contact = copy.deepcopy(self.valid_data)
        del data_with_invalid_sales_contact['sales_contact']
        data_with_invalid_sales_contact['sales_contact'] = 'invalid_data'
        serializer = self.serializer(data=data_with_invalid_sales_contact)
        assert not serializer.is_valid()
        assert serializer.errors['sales_contact']
        # assert serializer.errors['incorrect_type'] == 'Incorrect type. Expected pk value, received str.'
