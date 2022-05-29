import pytest
import copy
from datetime import datetime
from authentication.models import User
from clients.models import Client, Contract, Event
from clients.serializers import ContractDetailSerializer


class TestContractDetailSerializer:

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
                                               payment_due="2022-05-12 10:00:00")
        cls.event = Event.objects.create(support_contact=cls.supporter,
                                         event_status='In progress',
                                         attendees=50,
                                         event_date="2022-07-18 19:00:00",
                                         notes="birthday",
                                         contract=cls.contract,
                                         client=cls.client,
                                         )

        cls.serializer = ContractDetailSerializer
        payment_due = datetime.now()
        cls.valid_data = {'sales_contact': cls.sailor.id,
                          'client': cls.client.id,
                          'status': 0,
                          'amount': '100.00',
                          'payment_due': payment_due,
                          'event': cls.event.pk
                          }

    @pytest.mark.django_db
    def test_valid_serializer(self):
        serializer = self.serializer(data=self.valid_data)
        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_serializer_missing_required_field(self):
        """Test if all required fields are ok"""
        # missing status
        # data_without_status = copy.deepcopy(self.valid_data)
        # del data_without_status['status']
        # serializer = self.serializer(data=data_without_status)
        # assert not serializer.is_valid()
        # assert serializer.errors == {'status': ['This field is required.']}

        # missing amount
        data_without_amount = copy.deepcopy(self.valid_data)
        del data_without_amount['amount']
        serializer = self.serializer(data=data_without_amount)
        assert not serializer.is_valid()
        assert serializer.errors == {'amount': ['This field is required.']}

        # missing payment_due
        data_without_payment_due = copy.deepcopy(self.valid_data)
        del data_without_payment_due['payment_due']
        serializer = self.serializer(data=data_without_payment_due)
        assert not serializer.is_valid()
        assert serializer.errors == {'payment_due': ['This field is required.']}
    
        # missing sales_contact
        # data_without_sales_contact = copy.deepcopy(self.valid_data)
        # del data_without_sales_contact['sales_contact']
        # serializer = self.serializer(data=data_without_sales_contact)
        # assert not serializer.is_valid()
        # assert serializer.errors == {'sales_contact': ['This field is required.']}

        # missing client
        data_without_client = copy.deepcopy(self.valid_data)
        del data_without_client['client']
        serializer = self.serializer(data=data_without_client)
        assert not serializer.is_valid()
        assert serializer.errors == {'client': ['This field is required.']}

    @pytest.mark.django_db
    def test_invalid_field(self):
        """Test if all required fields are ok"""
        # status is boolean
        data_status_not_boolean = copy.deepcopy(self.valid_data)
        del data_status_not_boolean['status']
        data_status_not_boolean['status']= 12
        serializer = self.serializer(data=data_status_not_boolean)
        assert not serializer.is_valid()
        assert serializer.errors == {'status': ['Must be a valid boolean.']}

        # amount is decimal
        data_is_2decimal = copy.deepcopy(self.valid_data)
        del data_is_2decimal['amount']
        data_is_2decimal['amount'] = 'number'
        serializer = self.serializer(data=data_is_2decimal)
        assert not serializer.is_valid()
        assert serializer.errors == {'amount': ['A valid number is required.']}

        # amount is decimal with 2 numbers
        data_is_2decimal = copy.deepcopy(self.valid_data)
        del data_is_2decimal['amount']
        data_is_2decimal['amount'] = float(12.235)
        serializer = self.serializer(data=data_is_2decimal)
        assert not serializer.is_valid()
        assert serializer.errors == {'amount': ['Ensure that there are no more than 2 decimal places.']}

    #     data_with_too_long_mobile = copy.deepcopy(self.valid_data)
    #     del data_with_too_long_mobile['mobile']
    #     data_with_too_long_mobile['mobile'] = 'a_mobile_name_very_very_very_long'
    #     serializer = self.serializer(data=data_with_too_long_mobile)
    #     assert not serializer.is_valid()
    #     assert serializer.errors == {'mobile': ['Ensure this field has no more than 20 characters.']}
    #
    # @pytest.mark.django_db
    # def test_invalid_datatype_sales_contact(self):
    #     data_with_invalid_sales_contact = copy.deepcopy(self.valid_data)
    #     del data_with_invalid_sales_contact['sales_contact']
    #     data_with_invalid_sales_contact['sales_contact'] = 'invalid_data'
    #     serializer = self.serializer(data=data_with_invalid_sales_contact)
    #     assert not serializer.is_valid()
    #     assert serializer.errors == {'sales_contact': ['Incorrect type. Expected pk value, received str.']}
