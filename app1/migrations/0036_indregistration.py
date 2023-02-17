# Generated by Django 4.1.3 on 2023-02-08 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0035_remove_event_max_teams_event_event_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.event')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.player')),
            ],
        ),
    ]
