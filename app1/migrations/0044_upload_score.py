# Generated by Django 4.1.4 on 2023-02-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0043_remove_upload_file_frame'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
