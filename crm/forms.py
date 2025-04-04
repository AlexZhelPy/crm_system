from django import forms
from .models.services import Service
from .models.campaigns import Campaign
from .models.contracts import Contract
from .models.clients import Client
from .models.leads import Lead

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'service', 'channel', 'budget']

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'email', 'campaign']

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'  # Django ожидает ISO-формат (гггг-мм-дд)
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['lead', 'contract']