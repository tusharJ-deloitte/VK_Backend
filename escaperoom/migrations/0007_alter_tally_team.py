# Generated by Django 4.1.5 on 2023-01-23 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_remove_escaperoomquestions_escape_room_and_more'),
        ('escaperoom', '0006_tally'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tally',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.team'),
        ),
    ]
