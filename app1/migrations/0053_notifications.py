# Generated by Django 3.2.16 on 2023-02-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0052_remove_upload_uploaded_file_alter_event_created_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.TextField()),
                ('message', models.TextField()),
                ('sent', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
