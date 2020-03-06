from django.urls import path

from .views import *

urlpatterns = [
    path('messenger/', MessengerView.as_view(), name='messenger'),
]