# Generated by Django 5.1.5 on 2025-02-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0006_remove_issue_created_at_remove_issue_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
