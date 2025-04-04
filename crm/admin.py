from django.contrib import admin
from .models.campaigns import Campaign
from .models.clients import Client
from .models.contracts import Contract
from .models.leads import Lead
from .models.services import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'channel', 'budget')
    list_filter = ('service', 'channel')
    search_fields = ('name',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'campaign', 'is_converted')
    list_filter = ('campaign', 'is_converted')
    search_fields = ('full_name', 'phone', 'email')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'start_date', 'end_date', 'amount')
    list_filter = ('service', 'start_date')
    search_fields = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('lead', 'contract', 'created_at')
    list_filter = ('contract__service',)
    search_fields = ('lead__full_name',)
