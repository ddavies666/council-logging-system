# Generated by Django 5.1.5 on 2025-02-03 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_issue_contact_email_issue_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="predicted_label",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
