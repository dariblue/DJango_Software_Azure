import logging
from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', { 'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'


class DestinationCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description', 'latitude', 'longitude']
    # success_message = 'Destination "%(name)s" created successfully.'

class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description', 'latitude', 'longitude']
    # success_message = 'Destination "%(name)s" updated successfully.'

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    def form_valid(self, form):
        response = super().form_valid(form)

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        cruise = form.cleaned_data['cruise']
        notes = form.cleaned_data['notes']

        subject = f"New info request: {name}"
        message = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Cruise: {cruise.name}\n"
            f"Notes: {notes}"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.DEFAULT_INFO_EMAIL],
                fail_silently=False
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("Error sending email")
            messages.error(self.request, "The request was saved but the email could not be sent.")

        return response

