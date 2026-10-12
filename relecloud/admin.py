from django.contrib import admin
from . import models

@admin.register(models.Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name', 'description')

@admin.register(models.Cruise)
class CruiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'departure_date', 'return_date')
    search_fields = ('name', 'description')

@admin.register(models.InfoRequest)
class InfoRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'cruise')
    search_fields = ('name', 'email', 'notes')
