import pytest
from clients.models import Client, Contract, Event
from authentication.models import User


class TestModelClients:
    """Test the client model"""

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
                                               payment_due="2022-05-12 10:00:00")
        cls.event = Event.objects.create(support_contact=cls.supporter,
                                         event_status='In progress',
                                         attendees=50,
                                         event_date="2022-07-18 19:00:00",
                                         notes="birthday",
                                         contract=cls.contract,
                                         client=cls.client,
                                         )

    @pytest.mark.django_db
    def test_create_client(self):
        assert str(self.client) == "John Doe(Doe Enterprise) - contact: Sailor1"

    @pytest.mark.django_db
    def test_create_contract(self):
        assert str(self.contract) == "Contrat 2: John Doe(Doe Enterprise) - contact: Sailor1 for 100.0$"

    @pytest.mark.django_db
    def test_create_event_(self):
        assert str(self.event) == "3- for John Doe the 2022-07-18 19:00:00 - supporter: Supporter1"
