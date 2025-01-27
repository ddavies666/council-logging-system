from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    #return HttpResponse("<h1>Welcome to My Django Web App!</h1>")
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def report_issue(request):
    return render(request, 'report_issue.html')


def view_issues(request):
    return render(request, 'view_issues.html')
