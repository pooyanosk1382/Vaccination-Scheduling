from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from campaign.models import Campaign, Slot
from vacciation.models import Vaccination
from campaign.forms import CampaignForm, SlotForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class CampaignListView(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = "campaign/campaign-list.html"
    paginate_by = 10
    ordering = ["-id"]


class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = "campaign/campaign-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(campaign=self.kwargs["pk"]).count()
        return context


class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ("campaign.add_campaign",)
    template_name = "campaign/campaign-create.html"
    success_message = "Campaign created successfully"
    success_url = reverse_lazy("campaign:campaign-list")


class CampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ("campaign.change_campaign",)
    template_name = "campaign/campaign-update.html"
    success_message = "Campaign updated successfully"
    success_url = reverse_lazy("campaign:campaign-list")


class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Campaign
    template_name = "campaign/campaign-delete.html"
    permission_required = ("campaign.delete_campaign",)
    success_message = "Campaign deleted successfully"
    success_url = reverse_lazy("campaign:campaign-list")


class SlotListView(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "campaign/slot-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Slot.objects.filter(campaign=self.kwargs["campaign_id"]).order_by("id")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context


class SlotDetailView(LoginRequiredMixin, generic.DetailView):
    model = Slot
    template_name = "campaign/slot-detail.html"


class SlotCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Slot
    form_class = SlotForm
    template_name = "campaign/slot-create.html"
    permission_required = ("campaign.add_slot",)
    success_message = "Slot created successfully"

    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(id=self.kwargs["campaign"])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs