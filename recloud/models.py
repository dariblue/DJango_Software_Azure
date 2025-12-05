from django.db import models
from django.urls import reverse

from django.conf import settings
from django.db.models import Avg, Q



# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    latitude = models.FloatField(
        blank=True, 
        null=True
        )
    longitude = models.FloatField(
        blank=True,
        null=True
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={"pk": self.pk})
    
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    def reviews_count(self):
        return self.reviews.count()

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
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    departure_date = models.DateField(
        blank=False,
        null=False
    )
    return_date = models.DateField(
        blank=False,
        null=False
        )
    
    def __str__(self):
        return self.name
    
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    def reviews_count(self):
        return self.reviews.count()

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )

RATING_CHOICES = [
    (1, '1 ★'),
    (2, '2 ★★'),
    (3, '3 ★★★'),
    (4, '4 ★★★★'),
    (5, '5 ★★★★★'),
]


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,  #QUITAR CUANDO PONGAMOS LOGIN
        blank=True, #QUITAR CUANDO PONGAMOS LOGIN
    )
    destination = models.ForeignKey(
        'Destination',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    cruise = models.ForeignKey(
        'Cruise',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.destination:
            target = self.destination.name
        else:
            target = self.cruise.name
        return f'{self.user} -> {target} ({self.rating})'
