from django.shortcuts import render, redirect, get_object_or_404
from .models import Issue
from .forms import IssueForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    # Fetch all issues from the database
    issues = Issue.objects.all()  # or any other filter/query

    # Pass the issues to the template
    return render(request, 'home.html', {'issues': issues})


def issue_map(request):
    issues = Issue.objects.all()  # or any other filter/query

    # Pass the issues to the template
    return render(request, 'issue_map.html', {'issues': issues})


@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)  # Include request.FILES to handle image upload
        if form.is_valid():  # This validates the form and the file
            issue = form.save(commit=False)  # Don't save to DB yet, we need to extract GPS data

            # Extract GPS data from image (if available)
            lat, lon = issue.extract_gps_from_image()
            if lat and lon:
                issue.latitude = lat
                issue.longitude = lon
                print(f'GPS data extracted - Latitude: {lat}, Longitude: {lon}')
            else:
                print('No GPS data found in the image.')

            # Now save the issue after extracting GPS data
            issue.save()

            # Redirect after saving the issue
            return redirect('issue_submitted')  # Adjust to your desired URL after submission
    else:
        form = IssueForm()

    print(form.errors)  # Log any form validation errors

    return render(request, 'report_issue.html', {'form': form})


def submitted_issue(request):
    return render(request, 'issue_submitted.html')


def view_issues(request):
    issues = Issue.objects.all()
    return render(request, 'view_issues.html', {'issues': issues})


@login_required
def assigned_issues(request):
    # Check if the user is a staff member
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Filter issues assigned to the logged-in user
    issues = Issue.objects.filter(assigned_to=request.user)

    return render(request, 'assigned_issues.html', {'issues': issues})


def login_user(request):
    """
    Handles user login

    If the login form is valid and credentials match those on the system,
    this will successfully log the user in and redirect the user to the 
    hompeage.

    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': form, 'register_form': UserCreationForm()})


def register_user(request):
    """
    Handles user registration

    If the registration form is valid, it will save the user and their details
    to the database for future login access. Redirecting the user to the homepage
    now logged in.

    If the form in not valid, the data is not saved to the database and the user
    will be prompted to redo the form

    """
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
    """
    Logout Current User

    Logs the current user out of the system and redirects them to the homepage.

    """
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


@login_required
def update_issue(request, issue_id):
    # Fetch the issue object
    issue = get_object_or_404(Issue, pk=issue_id)
    
    # Check if the user is staff (for staff-only access)
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to update this issue.")

    # If the request is a POST, the form will be filled with existing data
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            form.save()  # Save the updated issue
            return redirect('view_issues')  # Redirect back to the issues page
    else:
        form = IssueForm(instance=issue)  # Populate the form with existing issue data

    return render(request, 'update_issue.html', {'form': form, 'issue': issue})


# Delete an issue - staff only
@login_required
def delete_issue(request, issue_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    issue = get_object_or_404(Issue, id=issue_id)
    issue.delete()
    return redirect('view_issues')