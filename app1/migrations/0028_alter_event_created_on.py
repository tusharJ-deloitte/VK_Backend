# Generated by Django 4.1.4 on 2023-02-02 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_alter_event_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 17, 50, 41, 750624)),
        ),
    ]
