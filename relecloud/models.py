from django.db import models
from django.urls import reverse

class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'pk': self.pk})


class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises',
    )
    departure_date = models.DateField(
        null=False,
        blank=False,
    )
    return_date = models.DateField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cruise_detail', kwargs={'pk': self.pk})


class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT,
    )
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.name} ({self.cruise})"
