from django.db import models

# Create your models here.


class Vaccine(models.Model):
    name = models.CharField("Vaccine Name", max_length=32)
    description = models.TextField(max_length=1024)
    numberOfDoses = models.IntegerField(default=1)
    interval = models.IntegerField(default=0, help_text="Please provide interval in days")
    storageTemperature = models.IntegerField(null=True, blank=True, help_text="Provide the temperature in Celsius")
    minimumAge = models.IntegerField(default=0)

    def __str__(self):
        return self.name