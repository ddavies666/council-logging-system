# myapp/urls.py

from django.urls import path
from . import views  # Import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Map the root URL to the 'home' view
    path('login/', views.login, name='login')
]
