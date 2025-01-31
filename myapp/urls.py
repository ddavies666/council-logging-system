# myapp/urls.py

from django.urls import path
from . import views  # Import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Map the root URL to the 'home' view
    path('login/', views.login_view, name='login'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('view-issues/', views.view_issues, name='view_issues'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('issue_management/', views.issue_management, name='issue_management')
]
