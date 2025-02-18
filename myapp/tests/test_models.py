import pytest
from myapp.models import Issue
from django.utils.timezone import now
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS 

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
    assert issue.latitude == 51.19158
    assert issue.title == str(issue)  # Test for __str__ method


@pytest.mark.django_db
def test_extract_gps_from_image():

    image = "myapp\\tests\\media\\graffiti1.jpg"
    img = Image.open(image)
    exif_data = img._getexif()
    
    if not exif_data:
        assert None

    
