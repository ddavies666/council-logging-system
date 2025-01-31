from django.shortcuts import render, redirect
from .models import Issue
from .forms import IssueForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'home.html')


@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)  # include request.FILES to handle the image upload
        if form.is_valid():  # This validates the form and the file
            form.save()  # Save the issue to the database
            return redirect('home')  # Redirect to home or another page after saving
    else:
        form = IssueForm()

    return render(request, 'report_issue.html', {'form': form})


def view_issues(request):
    issues = Issue.objects.all()
    return render(request, 'view_issues.html', {'issues': issues})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': form, 'register_form': UserCreationForm()})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registering
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'login.html', {'login_form': AuthenticationForm(), 'register_form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage after logout


# Ensure only staff can access the issue management page
@login_required
def issue_management(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    # Logic to show the issues for management, e.g., retrieving unresolved issues
    issues = Issue.objects.filter(status='open')  # Just an example, adjust as necessary
    return render(request, 'issue_management.html', {'issues': issues})