# Generated by Django 3.2.16 on 2023-01-17 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_event_cur_participation'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Yet To Start', 'yet to start'), ('Active', 'active'), ('Elapsed', 'elapsed')], default='Yet To Start', max_length=20),
        ),
        migrations.AddField(
            model_name='team',
            name='team_score',
            field=models.IntegerField(default=0),
        ),
    ]