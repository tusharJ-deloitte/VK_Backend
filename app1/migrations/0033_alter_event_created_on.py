# Generated by Django 4.1.3 on 2023-02-08 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_auto_20230203_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 13, 0, 17, 939751)),
        ),
    ]
