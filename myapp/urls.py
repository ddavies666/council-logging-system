# myapp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),  # Map the root URL to the 'home' view
    path('login/', views.login_user, name='login'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('view-issues/', views.view_issues, name='view_issues'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('issue-management/', views.issue_management, name='issue_management'),
    path('update-issue/<int:issue_id>/', views.update_issue, name='update_issue'),
    path('delete-issue/<int:issue_id>/', views.delete_issue, name='delete_issue'),
    path('assigned-issues/', views.assigned_issues, name='assigned_issues'),
    path('submitted-issue/', views.submitted_issue, name='issue_submitted'),
    path('issue-map/', views.issue_map, name='issue_map'),
    path('issue/<int:issue_id>/analysis', views.submit_analysis, name='submit_analysis'),
    path('view-analysis/', views.view_analysis, name='view_analysis'),
    path('analysis/update/<int:analysis_id>/', views.update_analysis, name='update_analysis'),
    path('analysis/delete/<int:analysis_id>/', views.delete_analysis, name='delete_analysis'),
    path('export-analysis-report/', views.export_analysis_report, name='export_analysis_report')]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)