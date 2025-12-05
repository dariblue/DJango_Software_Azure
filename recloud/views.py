from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# LOGIN --> cuando pongamos el login, descomenta la siguiente línea
# from django.contrib.auth.mixins import LoginRequiredMixin


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.order_by('-created_at')
        return context

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.order_by('-created_at')
        return context

#Reviews

# LOGIN: cuando el login sea obligatorio para opinar:
# 1) hereda de LoginRequiredMixin, generic.CreateView
#    class DestinationReviewCreateView(LoginRequiredMixin, generic.CreateView):
# 2) configurar LOGIN_URL en settings.py
class DestinationReviewCreateView(generic.CreateView):
    model = models.Review
    fields = ['rating', 'comment']
    template_name = 'review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.destination = get_object_or_404(models.Destination, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Si en el futuro tienes login, esto guardará el usuario;
        # de momento puede quedar a null sin problema.
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        form.instance.destination = self.destination
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = self.destination
        return context

    def get_success_url(self):
        return self.destination.get_absolute_url()


class CruiseReviewCreateView(generic.CreateView):
    model = models.Review
    fields = ['rating', 'comment']
    template_name = 'review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.cruise = get_object_or_404(models.Cruise, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        form.instance.cruise = self.cruise
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = self.cruise
        return context

    def get_success_url(self):
        from django.urls import reverse
        return reverse('cruise_detail', kwargs={'pk': self.cruise.pk})



#Request de info
class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'
