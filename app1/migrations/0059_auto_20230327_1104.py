# Generated by Django 3.2.16 on 2023-03-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0058_player_event_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='last_modified',
        ),
        migrations.AddField(
            model_name='quiz',
            name='time_modified',
            field=models.TextField(blank=True, null=True),
        ),
    ]
