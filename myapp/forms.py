from django import forms
from .models import Issue
from django.contrib.auth.models import User


class IssueForm(forms.ModelForm):
    """
    Class to represent IssueForm
    """
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="Select Assignee"
    )

    status = forms.ChoiceField(
        choices=Issue.STATUS_CHOICES,
        required=False
        )

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'assigned_to', 'location', 'contact_email', 'image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.extract_gps_from_image()
        if commit:
            instance.save()
        return instance
