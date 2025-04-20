from .views import campaigns, clients, contracts, leads, services, stats
from django.urls import path

urlpatterns = [
    # Services
    path("services/", services.ServiceListView.as_view(), name="service_list"),
    path("services/<int:pk>/", services.ServiceDetailView.as_view(), name="service_detail"),
    path("services/create/", services.ServiceCreateView.as_view(), name="service_create"),
    path("services/<int:pk>/update/", services.ServiceUpdateView.as_view(), name="service_update"),
    path("services/<int:pk>/delete/", services.ServiceDeleteView.as_view(), name="service_delete"),
    # Campaigns
    path("campaigns/", campaigns.CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/<int:pk>/", campaigns.CampaignDetailView.as_view(), name="campaign_detail"),
    path("campaigns/create/", campaigns.CampaignCreateView.as_view(), name="campaign_create"),
    path("campaigns/<int:pk>/update/", campaigns.CampaignUpdateView.as_view(), name="campaign_update"),
    path("campaigns/<int:pk>/delete/", campaigns.CampaignDeleteView.as_view(), name="campaign_delete"),
    # Leads
    path("leads/", leads.LeadListView.as_view(), name="lead_list"),
    path("leads/<int:pk>/", leads.LeadDetailView.as_view(), name="lead_detail"),
    path("leads/create/", leads.LeadCreateView.as_view(), name="lead_create"),
    path("leads/<int:pk>/update/", leads.LeadUpdateView.as_view(), name="lead_update"),
    path("leads/<int:pk>/delete/", leads.LeadDeleteView.as_view(), name="lead_delete"),
    path("leads/<int:pk>/convert/", leads.LeadConvertView.as_view(), name="lead_convert"),
    # Contracts
    path("contracts/", contracts.ContractListView.as_view(), name="contract_list"),
    path("contracts/<int:pk>/", contracts.ContractDetailView.as_view(), name="contract_detail"),
    path("contracts/create/", contracts.ContractCreateView.as_view(), name="contract_create"),
    path("contracts/<int:pk>/update/", contracts.ContractUpdateView.as_view(), name="contract_update"),
    path("contracts/<int:pk>/delete/", contracts.ContractDeleteView.as_view(), name="contract_delete"),
    # Clients
    path("clients/", clients.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/", clients.ClientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/update/", clients.ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", clients.ClientDeleteView.as_view(), name="client_delete"),
    # Stats
    path("stats/", stats.CampaignStatsView.as_view(), name="campaign_stats"),
]
