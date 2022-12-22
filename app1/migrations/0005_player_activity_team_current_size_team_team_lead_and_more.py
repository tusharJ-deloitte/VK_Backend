# Generated by Django 4.1.3 on 2022-12-21 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0004_alter_category_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='activity',
            field=models.ManyToManyField(to='app1.activity'),
        ),
        migrations.AddField(
            model_name='team',
            name='current_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='team_lead',
            field=models.TextField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='activity',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='activity',
            field=models.ManyToManyField(null=True, to='app1.activity'),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ManyToManyField(to='app1.team'),
        ),
    ]
