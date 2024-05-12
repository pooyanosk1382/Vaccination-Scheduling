from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from vaccine.models import Vaccine
from campaign.models import Campaign, Slot
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone


class ChooseVaccine(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    template_name = "vaccination/choose-vaccine.html"
    paginate_by = 10
    ordering = ["name"]


class ChooseCampaign(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = "vaccination/choose-campaign.html"
    paginate_by = 10
    ordering = ["start_date"]

    def get_queryset(self):
        return super().get_queryset().filter(vaccine=self.kwargs["vaccine_id"])


class ChooseSlot(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "vaccination/choose-slot.html"
    paginate_by = 10
    ordering = ["date"]

    def get_queryset(self):
        return super().get_queryset().filter(campaign=self.kwargs["campaign_id"], date__gte=timezone.now())
