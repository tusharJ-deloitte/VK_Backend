# Generated by Django 4.1.4 on 2023-02-10 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0040_upload_event_upload_is_uploaded_upload_uploaded_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='file_size',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
