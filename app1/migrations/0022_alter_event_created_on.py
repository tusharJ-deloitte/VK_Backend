# Generated by Django 3.2.16 on 2023-02-01 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_alter_event_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 1, 10, 42, 9, 24463)),
        ),
    ]