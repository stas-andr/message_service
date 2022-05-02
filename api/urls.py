from django.urls import path

from .views import clients, client_detail, mail_lists

urlpatterns = [
    path('mail_lists/', mail_lists),
    path('clients/<int:pk>/', client_detail),
    path('clients/', clients)
]