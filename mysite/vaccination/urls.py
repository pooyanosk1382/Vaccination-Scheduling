from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = {
    path("choose-vaccine/", views.ChooseVaccine.as_view(), name="choose-vaccine"),
    path("choose-campaign/<int:vaccine_id>", views.ChooseCampaign.as_view(), name="choose-campaign"),
    path("choose-slot/<int:campaign_id>", views.ChooseSlot.as_view(), name="choose-slot"),
}