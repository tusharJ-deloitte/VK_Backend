# Generated by Django 4.1.3 on 2023-01-20 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_alter_event_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 20, 17, 35, 40, 955474)),
        ),
    ]
