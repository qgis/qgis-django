# Generated by Django 2.2 on 2020-11-08 11:00

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("styles", "0004_auto_20201108_0742"),
    ]

    operations = [
        migrations.AddField(
            model_name="style",
            name="modified_date",
            field=models.DateTimeField(
                default=datetime.datetime(2020, 11, 8, 11, 0, 41, 965734),
                editable=False,
                help_text="The upload date. Automatically added on file upload.",
                verbose_name="Modified on",
            ),
            preserve_default=False,
        ),
    ]
