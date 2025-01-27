# myapp/urls.py

from django.urls import path
from . import views  # Import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Map the root URL to the 'home' view
    path('login/', views.login, name='login'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('view-issues/', views.view_issues, name='view_issues')
]
