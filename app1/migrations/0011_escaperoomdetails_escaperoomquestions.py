# Generated by Django 4.1.5 on 2023-01-17 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_event_cur_participation'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscapeRoomDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=20)),
                ('bg_image', models.TextField()),
                ('number_of_questions', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EscapeRoomQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('number_of_images', models.IntegerField()),
                ('images', models.JSONField(null=True)),
                ('question_type', models.IntegerField()),
                ('question', models.TextField()),
                ('options', models.JSONField(null=True)),
                ('answers', models.TextField()),
                ('hints', models.TextField(null=True)),
                ('escape_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.escaperoomdetails')),
            ],
        ),
    ]
