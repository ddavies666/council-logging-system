from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
from PIL import Image
from typing import List, Tuple


class Issue(models.Model):
    STATUS_CHOICES: list[Tuple[str, str]] = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    # Main fields
    title: str = models.CharField(max_length=255)
    created_at: datetime = models.DateTimeField(auto_now_add=True, null=True)
    description: str = models.TextField()
    status: str = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    assigned_to: str = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    location: str = models.CharField(max_length=255, blank=True, null=True)
    contact_email: str = models.EmailField(blank=True, null=True)

    # Image field
    image: Image.Image = models.ImageField(upload_to='issue_images/', blank=True, null=True)

    # fields for GPS coordinates
    latitude: float = models.FloatField(blank=True, null=True)
    longitude: float = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def extract_gps_from_image(self) -> Tuple[float]:
        """
        Extracts GPS data from the image if available and saves lat/lon to model.
        """

        if not self.image:
            return

        try:
            img = Image.open(self.image)
            exif_data = img._getexif()

            if not exif_data:
                return None, None  # No GPS data

            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for t in value:
                        gps_info[GPSTAGS.get(t, t)] = value[t]

            if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
                lat = self._convert_to_decimal(gps_info['GPSLatitude'], gps_info.get('GPSLatitudeRef', 'N'))
                lon = self._convert_to_decimal(gps_info['GPSLongitude'], gps_info.get('GPSLongitudeRef', 'E'))

                # Save the coordinates to the model's fields
                self.latitude = lat
                self.longitude = lon
                self.save()  # Save the model with updated coordinates

                return lat, lon  # Return the coordinates

        except Exception as e:
            print("Error extracting EXIF data:", e)

        return None, None  # Return None if no data found

    def _convert_to_decimal(self, coord: float, ref: str) -> float:
        """
        Convert DMS coordinates to decimal
        """
        decimal = coord[0] + coord[1] / 60.0 + coord[2] / 3600.0
        if ref in ['S', 'W']:
            decimal *= -1
        return decimal


class Analysis(models.Model):
    ENERGY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    ACTION_CHOICES = [
        ('repair', 'Repair'),
        ('replace', 'Replace'),
        ('monitor', 'Monitor'),
        ('refer', 'Refer to External Team')
    ]

    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='analysis')
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE, db_column='staff_member_id')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    estimated_cost = models.IntegerField(help_text="Estimated cost in GBP", null=True, blank=True)
    estimated_time = models.IntegerField(help_text="Estimated time to fix in days", null=True, blank=True)
    energy_required = models.CharField(max_length=10, choices=ENERGY_CHOICES, default='medium', null=True)
    priority_level = models.IntegerField(help_text="Priority level (1-10)", null=True, blank=True)
    recommended_action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='repair')
    environmental_impact = models.IntegerField(help_text="Environmental impact (0-100)", null=True, blank=True)
    supporting_document = models.FileField(upload_to='analysis_docs/', null=True, blank=True)

    def __str__(self):
        return f'Analysis by {self.staff_member.username} on {self.issue.title}'
