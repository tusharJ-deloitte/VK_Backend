# Generated by Django 3.2.16 on 2023-04-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysteryroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysteryroom',
            name='total_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]