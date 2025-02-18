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
def test_login_view(client, django_user_model):
    django_user_model.objects.create_user(username="testuser", password="password")
    response = client.post(
        reverse("login"), {"username": "testuser", "password": "password"}
    )
    assert response.status_code == 302  # Redirect to home


@pytest.mark.django_db
def test_register_view(client):
    response = client.post(
        reverse("register"),
        {"username": "newuser", "password1": "password", "password2": "password"},
    )
    assert response.status_code == 302  # Redirect to home


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