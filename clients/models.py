from django.db import models
from authentication.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.company_name}) - contact: {self.sales_contact.username}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_sailor')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts_client')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(verbose_name='signed')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    payment_due = models.DateTimeField()

    def __str__(self):
        return f"Contrat {self.id}: {self.client} for {self.amount}$"


class Event(models.Model):
    IN_PROGRESS = 'IN PROGRESS'
    FINISHED = 'FINISHED'

    ROLE_CHOICES = (
        (IN_PROGRESS, 'In progress'),
        (FINISHED, 'Finished'),
    )

    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, primary_key=True, related_name='event')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='events_client')
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_supporter')
    event_status = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk}- for {self.contract.client.first_name} {self.contract.client.last_name} " \
               f"the {self.event_date} - supporter: {self.support_contact.username}"
