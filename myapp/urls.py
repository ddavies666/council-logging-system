# myapp/urls.py

from django.urls import path
from . import views  # Import views

urlpatterns = [
    path('', views.home),  # Map the root URL to the 'home' view
]
