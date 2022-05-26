import datetime

from django.urls import reverse_lazy, reverse
import pytest
from django import test
from clients.models import Client, Contract, Event
from authentication.models import User


class TestClientEndpoint:

    @classmethod
    def setup(cls):
        cls.sailor = User.objects.create_user(username='Sailor1',
                                              password='password1',
                                              role='SAILOR')
        cls.supporter1 = User.objects.create_user(username='Supporter1',
                                                  role='SUPPORT')
        cls.supporter2 = User.objects.create_user(username='Supporter2',
                                                  role='SUPPORT')
        cls.client = Client.objects.create(first_name='John',
                                           last_name='Doe',
                                           email='johndoe@test.com',
                                           phone='00632562',
                                           mobile='036479536',
                                           company_name='Doe Enterprise',
                                           sales_contact=cls.sailor)
        cls.client2 = Client.objects.create(first_name='John',
                                            last_name='Doe',
                                            email='johndoe@test.com',
                                            phone='00632562',
                                            mobile='036479536',
                                            company_name='Doe Enterprise',
                                            sales_contact=cls.sailor)
        cls.contract1 = Contract.objects.create(sales_contact=cls.sailor,
                                                client=cls.client,
                                                status=1,
                                                amount=100.00,
                                                payment_due=datetime.datetime.now())
        cls.contract2 = Contract.objects.create(sales_contact=cls.sailor,
                                                client=cls.client,
                                                status=1,
                                                amount=100.00,
                                                payment_due=datetime.datetime.now())
        cls.event1 = Event.objects.create(support_contact=cls.supporter1,
                                          event_status='In progress',
                                          attendees=50,
                                          event_date=datetime.datetime.now(),
                                          notes="birthday",
                                          contract=cls.contract1,
                                          client=cls.client,
                                         )
        cls.event2 = Event.objects.create(support_contact=cls.supporter1,
                                          event_status='In progress',
                                          attendees=50,
                                          event_date=datetime.datetime.now(),
                                          notes="birthday",
                                          contract=cls.contract2,
                                          client=cls.client,
                                          )

    def format_datetime(self, value):
        """ Return a type datetime in string"""
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @pytest.mark.django_db
    def test_display_list_of_client_with_sailor_authorization(self):
        client_test = test.Client()
        client_test.force_login(self.sailor)
        url = reverse_lazy('client-list')
        response = client_test.get(url)
        assert response.status_code == 200

        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.client.id,
                    'first_name': self.client.first_name,
                    'last_name': self.client.last_name,
                    'email': self.client.email,
                    'phone': self.client.phone,
                    'mobile': self.client.mobile,
                    'company_name': self.client.company_name,
                    'sales_contact': self.sailor.pk,
                },
                {
                    'id': self.client2.id,
                    'first_name': self.client2.first_name,
                    'last_name': self.client2.last_name,
                    'email': self.client2.email,
                    'phone': self.client2.phone,
                    'mobile': self.client2.mobile,
                    'company_name': self.client2.company_name,
                    'sales_contact': self.sailor.pk,
                }
            ]
        }
        assert response.json() == expected

    @pytest.mark.django_db
    def test_display_detail_of_clients_with_sailor_authorization(self):
        client_test = test.Client()
        client_test.force_login(self.sailor)
        url_detail = reverse('client-detail', kwargs={'pk': self.client.pk})
        response = client_test.get(url_detail)
        assert response.status_code == 200

        contract1 = {
            'pk': self.contract1.pk,
            'sales_contact': self.sailor.pk,
            'client': self.client.pk,
            'date_created': self.format_datetime(self.contract1.date_created),
            'date_updated': self.format_datetime(self.contract1.date_updated),
            'status': self.contract1.status,
            'amount': '100.00',
            'payment_due': self.format_datetime(self.contract1.payment_due),
            'event': self.event1.pk
        }
        contract2 = {
            'pk': self.contract2.pk,
            'sales_contact': self.sailor.pk,
            'client': self.client.pk,
            'date_created': self.format_datetime(self.contract2.date_created),
            'date_updated': self.format_datetime(self.contract2.date_updated),
            'status': self.contract2.status,
            'amount': '100.00',
            'payment_due': self.format_datetime(self.contract2.payment_due),
            'event': self.event2.pk
        }
        expected = {
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
            'contracts_client': [contract1, contract2],
        }
        print(response)
        assert response.json() == expected

    @pytest.mark.django_db
    def test_display_list_of_client_with_supporter_authorization(self):
        """A supporter can only access clients with events assigned to them."""
        client_test = test.Client()
        client_test.force_login(self.supporter1)
        url = reverse_lazy('client-list')
        response = client_test.get(url)
        assert response.status_code == 200

        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.client.id,
                    'first_name': self.client.first_name,
                    'last_name': self.client.last_name,
                    'email': self.client.email,
                    'phone': self.client.phone,
                    'mobile': self.client.mobile,
                    'company_name': self.client.company_name,
                    'sales_contact': self.sailor.pk,
                }]
        }
        assert response.json() == expected

    @pytest.mark.django_db
    def test_sailor_create_client(self):
        """ Only sailor can create client."""
        clients = Client.objects.all()
        first_name_list = [client.first_name for client in clients]
        new_client = {
            'first_name': 'new',
            'last_name': 'new_client',
            'email': 'new_client@test.com',
            'phone': '036489',
            'mobile': '03157',
            'company_name': 'New Client SA',
            'sales_contact': self.sailor.pk
        }

        client_test = test.Client()
        client_test.force_login(self.sailor)
        url = reverse_lazy('client-list')
        response = client_test.post(url, data=new_client)
        assert response.status_code == 201
        new_client_created = Client.objects.get(first_name='new')
        assert new_client_created.first_name == 'new'
        assert new_client_created.first_name not in first_name_list

    @pytest.mark.django_db
    def test_supporter_cannot_create_client(self):
        """ Only sailor can create client."""
        clients = Client.objects.all()
        first_name_list = [client.id for client in clients]
        assert 'new' not in first_name_list
        new_client = {
            'first_name': 'new',
            'last_name': 'new_client',
            'email': 'new_client@test.com',
            'phone': '036489',
            'mobile': '03157',
            'company_name': 'New Client SA',
            'sales_contact': self.sailor.pk
        }

        client_test = test.Client()
        client_test.force_login(self.supporter1)
        url = reverse_lazy('client-list')
        response = client_test.post(url, data=new_client)
        assert response.status_code == 403
        assert 'new' not in first_name_list

    @pytest.mark.django_db
    def test_sailor_can_update_only_their_client(self):

        # try to update a client to another sailor
        sailor2 = User.objects.create_user(username='sailor2',
                                           role='SAILOR')
        url_detail = reverse('client-detail', kwargs={'pk': self.client.pk})
        client_test = test.Client()
        client_test.force_login(sailor2)
        response = client_test.put(url_detail, params={'first_name': 'test',
                                                       'last_name': 'test',
                                                       'email': 'email@test.fr',
                                                       'mobile': '06354',
                                                       'company_name': 'test',
                                                       'sales_contact': sailor2.pk})
        assert response.status_code == 403
        client_first_name = Client.objects.get(id=self.client.pk)
        assert client_first_name.first_name == 'John'

    @pytest.mark.django_db
    def test_sailor_can_update_their_client(self):

        # update his own client
        client_test = test.Client()
        client_test.force_login(self.sailor)
        url_detail = reverse('client-detail', kwargs={'pk': self.client.pk})
        response = client_test.put(url_detail, {'first_name': 'test',
                                                'last_name': 'test',
                                                'email': 'email@test.fr',
                                                'phone': '0368',
                                                'mobile': '06354',
                                                'company_name': 'test',
                                                'sales_contact': self.sailor.pk
                                                }, content_type='application/json')
        print(response.content)
        assert response.status_code == 200
        client_data = Client.objects.get(id=self.client.pk)
        assert client_data.first_name == 'test'
