from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class Issue(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)

    # New fields for GPS coordinates
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

    def extract_gps_from_image(self):
        """Extracts GPS data from the image if available and saves lat/lon to model."""  
        if self.image:
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


    def _convert_to_decimal(self, coord, ref):
        """ Convert DMS coordinates to decimal """
        decimal = coord[0] + coord[1] / 60.0 + coord[2] / 3600.0
        if ref in ['S', 'W']:
            decimal *= -1
        return decimal
