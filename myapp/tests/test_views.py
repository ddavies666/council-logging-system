import pytest
from myapp.models import Issue
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Issue
from django.utils.timezone import now


@pytest.mark.django_db
def test_view_issues(client):
    Issue.objects.create(
        title="Graffiti on Wall",
        status="open",
    )
    response = client.get(reverse("view_issues"))

    assert response.status_code == 200
    assert "Graffiti on Wall" in response.content.decode()


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "issues" in response.context


@pytest.mark.django_db
def test_issue_map_view(client):
    response = client.get(reverse("issue_map"))
    assert response.status_code == 200
    assert "issues" in response.context


@pytest.mark.django_db
def test_report_issue_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")
    response = client.get(reverse("report_issue"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_report_issue_unauthenticated(client):
    response = client.get(reverse("report_issue"))
    assert response.status_code == 302  # Redirects to login


@pytest.mark.django_db
def test_submitted_issue_view(client):
    response = client.get(reverse("issue_submitted"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_assigned_issues_staff(client, django_user_model):
    staff_user = django_user_model.objects.create_user(
        username="staffuser", password="password", is_staff=True
    )
    client.login(username="staffuser", password="password")
    response = client.get(reverse("assigned_issues"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_assigned_issues_non_staff(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")
    response = client.get(reverse("assigned_issues"))
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
@pytest.mark.parametrize("username, password, expected_status_code, expected_redirect", [
    ('testuser', 'testpassword', 302, 'home'),  # Valid credentials, should redirect to home
    ('testuser', 'wrongpassword', 200, None),  # Invalid password, should stay on login page
    ('wronguser', 'testpassword', 200, None),  # Invalid username, should stay on login page

])
def test_login_user(client, username, password, expected_status_code, expected_redirect):

    # Create a test user
    User.objects.create_user(username='testuser', password='testpassword')

    # Post login data
    login_url = reverse('login')  # Adjust the URL name if necessary
    response = client.post(login_url, {'username': username, 'password': password})

    # Check status code and redirection
    assert response.status_code == expected_status_code

    if expected_redirect:
        # Check that we redirect to the homepage after successful login
        assert response.url.endswith(reverse(expected_redirect))
    else:
        # If no redirection, check the login page contains the login form
        assert 'name="username"' in response.content.decode()
        assert 'name="password"' in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("username, password1, password2, expected_status_code, expected_redirect, expected_error_message", [
    ('newuser', 'password', 'password', 302, 'home', None),  # Valid registration, should redirect to home
    ('newuser', 'password', 'differentpassword', 200, None, 'password2'),  # Password mismatch, should stay on the page
    ('existinguser', 'password', 'password', 200, None, 'username'),  # Username already exists, should stay on the page
])
def test_register_user(client, username, password1, password2, expected_status_code, expected_redirect, expected_error_message):
    # If username already exists, create the user first
    if expected_error_message == 'username':
        User.objects.create_user(username='existinguser', password='password')

    # Post registration data
    response = client.post(
        reverse("register"),
        {"username": username, "password1": password1, "password2": password2},
    )

    # Check the status code
    assert response.status_code == expected_status_code


@pytest.mark.django_db
def test_logout_view(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")
    response = client.get(reverse("logout"))
    assert response.status_code == 302  # Redirect to home


@pytest.mark.django_db
def test_issue_management_staff(client, django_user_model):
    staff_user = django_user_model.objects.create_user(
        username="staffuser", password="password", is_staff=True
    )
    client.login(username="staffuser", password="password")
    response = client.get(reverse("issue_management"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_issue_management_non_staff(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")
    response = client.get(reverse("issue_management"))
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_update_issue_staff(client, django_user_model):
    staff_user = django_user_model.objects.create_user(
        username="staffuser", password="password", is_staff=True
    )
    issue = Issue.objects.create(title="Old Issue", status="open", created_at=now())
    client.login(username="staffuser", password="password")
    response = client.post(
        reverse("update_issue", args=[issue.id]),
        {"title": "Updated Issue", "status": "closed"},
    )
    assert response.status_code == 302  # Redirect
    issue.refresh_from_db()
    assert issue.title == "Updated Issue"


@pytest.mark.django_db
def test_delete_issue_staff(client, django_user_model):
    staff_user = django_user_model.objects.create_user(
        username="staffuser", password="password", is_staff=True
    )
    issue = Issue.objects.create(title="Test Issue", status="open", created_at=now())
    client.login(username="staffuser", password="password")
    response = client.post(reverse("delete_issue", args=[issue.id]))
    assert response.status_code == 302  # Redirect
    assert not Issue.objects.filter(id=issue.id).exists()