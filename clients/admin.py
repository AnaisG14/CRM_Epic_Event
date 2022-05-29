from django.contrib import admin
from .models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):
    list_filter = ('sales_contact', 'date_created', 'status')


class ContractAdmin(admin.ModelAdmin):
    list_filter = ('client', 'date_created', 'status', 'payment_due', 'sales_contact')


class EventAdmin(admin.ModelAdmin):
    list_filter = ('client', 'support_contact', 'event_date')


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
