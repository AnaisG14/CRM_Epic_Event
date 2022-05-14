import datetime

from django.urls import reverse_lazy
import pytest
from django import test
from clients.models import Client, Contract, Event
from authentication.models import User


class TestClientEndpoint:

    @classmethod
    def setup(cls):
        cls.url = reverse_lazy('client-list')
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

    def format_datetime(self, value):
        """ Return a type datetime in string"""
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @pytest.mark.django_db
    def test_display_list_of_clients(self):
        client_test = test.Client()
        response = client_test.get(self.url)
        assert response.status_code == 200

        contract = {
            'pk': self.contract.pk,
            'sales_contact': self.sailor.pk,
            'client': self.client.pk,
            'date_created': self.format_datetime(self.contract.date_created),
            'date_updated': self.format_datetime(self.contract.date_updated),
            'status': True,
            'amount': '100.00',
            'payment_due': self.format_datetime(self.contract.payment_due),
            'event': self.event.pk
        }
        expected = [{
            'id': self.client.id,
            'first_name': self.client.first_name,
            'last_name': self.client.last_name,
            'email': self.client.email,
            'phone': self.client.phone,
            'mobile': self.client.mobile,
            'company_name': self.client.company_name,
            'date_created': self.format_datetime(self.client.date_created),
            'date_updated': self.format_datetime(self.client.date_updated),
            'sales_contact': self.sailor.pk,
            'contracts_client': [contract]
        }]

        assert response.json() == expected

#     def test_create(self):
#         # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
#         self.assertFalse(Category.objects.exists())
#         response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
#         # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
#         self.assertEqual(response.status_code, 405)
#         # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
#         self.assertFalse(Category.objects.exists())
#

