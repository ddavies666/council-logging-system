import pytest
from myapp.models import Issue
from django.utils.timezone import now


@pytest.mark.django_db
def test_issue_creation():
    issue = Issue.objects.create(
        title="Pothole on Main Street",
        description="Large pothole causing traffic issues",
        status="open",
        latitude=51.19158,
        longitude=0.276540,
        created_at=now()
    )
    assert issue.title == "Pothole on Main Street"
    assert issue.status == "open"
