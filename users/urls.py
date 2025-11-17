from django.urls import path, include
from rest_framework import routers
from users.views import LoginView

urlpatterns = [
    path('autenticate/', LoginView.as_view(), name='login'),
]

