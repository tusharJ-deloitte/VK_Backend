# Generated by Django 4.1.5 on 2023-01-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_escaperoomdetails_escaperoomquestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escaperoomquestions',
            name='images',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='escaperoomquestions',
            name='options',
            field=models.JSONField(blank=True, null=True),
        ),
    ]