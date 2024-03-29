import datetime

from django.urls import reverse_lazy, reverse
import pytest
from django import test
from clients.models import Client, Contract, Event
from authentication.models import User


class TestEventEndpoint:

    @classmethod
    def setup(cls):
        cls.sailor = User.objects.create_user(username='Sailor1',
                                              role='SAILOR')
        cls.supporter = User.objects.create_user(username='Supporter1',
                                                 role='SUPPORT')
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
    def test_display_list_of_event(self):
        client_test = test.Client()
        client_test.force_login(self.sailor)
        url = reverse_lazy('event-list')
        response = client_test.get(url)
        assert response.status_code == 200

        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'contract': self.event.contract.pk,
                    'date_created': self.format_datetime(self.event.date_created),
                    'date_updated': self.format_datetime(self.event.date_updated),
                    'client': self.client.pk,
                    'support_contact': self.supporter.pk,
                    'event_status': self.event.event_status,
                    'attendees': self.event.attendees,
                    'event_date': self.format_datetime(self.event.event_date),
                    'notes': self.event.notes
                }]
        }
        assert response.json() == expected

    @pytest.mark.django_db
    def test_display_detail_of_event(self):
        client_test = test.Client()
        client_test.force_login(self.sailor)
        url_detail = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = client_test.get(url_detail)
        assert response.status_code == 200

        expected = {
            'contract': self.contract.pk,
            'date_created': self.format_datetime(self.event.date_created),
            'date_updated': self.format_datetime(self.event.date_updated),
            'client': self.client.pk,
            'support_contact': self.supporter.pk,
            'event_status': self.event.event_status,
            'attendees': self.event.attendees,
            'event_date': self.format_datetime(self.event.event_date),
            'notes': self.event.notes
        }
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

