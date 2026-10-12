from django.db import models
from django.urls import reverse

class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Nombre",
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Latitud",
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Longitud",
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
        verbose_name="Descripcion",
    )

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"

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
        verbose_name="Nombre",
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
        verbose_name="Descripcion",
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises',
        verbose_name="Destinos",
    )
    departure_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Fecha de salida",
    )
    return_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Fecha de regreso",
    )

    class Meta:
        verbose_name = "Crucero"
        verbose_name_plural = "Cruceros"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cruise_detail', kwargs={'pk': self.pk})


class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Nombre completo",
    )
    email = models.EmailField(
        verbose_name="Correo electronico",
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT,
        verbose_name="Crucero",
    )
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
        verbose_name="Notas o preguntas",
    )

    class Meta:
        verbose_name = "Solicitud de informacion"
        verbose_name_plural = "Solicitudes de informacion"

    def __str__(self):
        return f"{self.name} ({self.cruise})"
