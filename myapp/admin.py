from django.contrib import admin
from .models import Issue, Analysis  # Import the models

# Register your models here.
admin.site.register(Issue)
admin.site.register(Analysis)
