# Generated by Django 5.1.5 on 2025-02-03 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_issue_predicted_label"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="issue",
            name="predicted_label",
        ),
    ]
