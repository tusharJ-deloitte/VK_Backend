# Generated by Django 4.1.4 on 2023-02-13 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0045_alter_upload_file_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
