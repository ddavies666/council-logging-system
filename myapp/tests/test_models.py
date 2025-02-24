import pytest
from myapp.models import Issue
from django.utils.timezone import now
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from unittest.mock import patch
from io import BytesIO


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "exif_data, expected_latitude, expected_longitude",
    [
        # Test 1: Valid GPS coordinates 
        ({
            34853: {
                2: [(40, 1, 0), (0, 1, 0)],  # Latitude 40°N
                4: [(75, 1, 0), (0, 1, 0)],  # Longitude 75°W
                1: 'N',  # Latitude hemisphere
                3: 'W'   # Longitude hemisphere
            }
        }, 40.0, -75.0),
        
        # Test 2: No GPS data (None)
        (None, None, None)
    ]
)
def test_extract_gps_from_image(exif_data, expected_latitude, expected_longitude):
    # Create an Issue object (without an image initially)
    issue = Issue.objects.create(title="Test Issue", description="Test description")

    # Mock Image.open and its _getexif method to return  exif_data
    with patch('PIL.Image.open') as mock_open:
        mock_image = mock_open.return_value
        if exif_data:
            mock_image._getexif.return_value = exif_data
        else:
            mock_image._getexif.return_value = None  

        # Simulate an image being uploaded to the 'image' field
        issue.image = BytesIO(b"fakeimage")  # Fake image content
        issue.extract_gps_from_image()  # Call the method to extract GPS

        # Assert that the latitude and longitude were set correctly
        assert issue.latitude == expected_latitude  
        assert issue.longitude == expected_longitude  