from django.urls import path

from .views import clients

urlpatterns = [
    path('clients/', clients)
]