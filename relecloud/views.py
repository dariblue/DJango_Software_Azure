from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from . import models

# Vistas sencillas
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})

# Vistas genericas de Destinos
class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class DestinationCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description', 'latitude', 'longitude']
    success_message = 'Destino "%(name)s" creado correctamente.'

class DestinationUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description', 'latitude', 'longitude']
    success_message = 'Destino "%(name)s" actualizado correctamente.'

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

# Vista de detalle de Crucero
class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

# Vista generica de InfoRequest (CreateView, redirige a 'index' con mensaje de exito)
class InfoRequestCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = '¡Muchas gracias, %(name)s! Hemos recibido tu solicitud de informacion.'
