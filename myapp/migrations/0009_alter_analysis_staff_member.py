# Generated by Django 5.1.5 on 2025-02-21 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0008_analysis"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="analysis",
            name="staff_member",
            field=models.ForeignKey(
                db_column="staff_member_id",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
