# Generated by Django 4.1.4 on 2023-02-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0051_merge_20230218_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='uploaded_file',
        ),
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.TextField(max_length=20),
        ),
    ]