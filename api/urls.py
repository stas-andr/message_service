from django.urls import path

from .views import ClientDetail
from .views import ClientList
from .views import MailListView
from .views import MailListDetail
from .views import MessageList

urlpatterns = [
    path('messages/', MessageList.as_view()),
    path('mail_lists/<int:pk>/', MailListDetail.as_view()),
    path('mail_lists/', MailListView.as_view()),
    path('clients/<int:pk>/', ClientDetail.as_view()),
    path('clients/', ClientList.as_view())
]