# Generated by Django 3.2.16 on 2023-03-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0055_event_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='task_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='event_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
