from django.urls import path

from .views import clients, client_detail, mail_lists, mail_list_detail

urlpatterns = [
    path('mail_lists/<int:pk>', mail_list_detail),
    path('mail_lists/', mail_lists),
    path('clients/<int:pk>/', client_detail),
    path('clients/', clients)
]