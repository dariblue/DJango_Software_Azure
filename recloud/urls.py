## APP (recloud)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destination/add', views.DestinationCreateView.as_view(), name='destination_form'),
    path('destination/<int:pk>/update', views.DestinationUpdateView.as_view(), name='destination_form'),
    path('destination/<int:pk>/delete', views.DestinationDeleteView.as_view(), name='destination_confirm_delete'),
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),

    # Reviews
    path('destination/<int:pk>/review', views.DestinationReviewCreateView.as_view(), name='destination_review'),
    path('cruise/<int:pk>/review', views.CruiseReviewCreateView.as_view(), name='cruise_review'),
]
