# Generated by Django 3.2.16 on 2023-04-03 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MysteryRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True, unique=True)),
                ('difficulty_level', models.CharField(choices=[('EASY', 'EASY'), ('MEDIUM', 'MEDIUM'), ('HARD', 'HARD')], default='EASY', max_length=20)),
                ('number_of_questions', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.TextField(blank=True, null=True)),
                ('last_modified', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MysteryRoomCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(default=0)),
                ('banner_image', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True, unique=True)),
                ('number_of_team_members', models.IntegerField(blank=True, default=0, null=True)),
                ('number_of_mystery_rooms', models.IntegerField(default=0)),
                ('theme', models.TextField(blank=True, null=True)),
                ('created_on', models.TextField(blank=True, null=True)),
                ('last_modified', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MysteryRoomQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField(blank=True, null=True)),
                ('question_text', models.TextField(blank=True, null=True)),
                ('question_image', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('hint_text', models.TextField(blank=True, null=True)),
                ('hint_image', models.TextField(blank=True, null=True)),
                ('question_type', models.CharField(choices=[('MCQ', 'MCQ'), ('Checkbox', 'Checkbox'), ('TextField', 'TextField')], default='MCQ', max_length=20)),
                ('total_time', models.IntegerField(blank=True, null=True)),
                ('mystery_room_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroomcollection')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroom')),
            ],
        ),
        migrations.CreateModel(
            name='MysteryRoomOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroomquestion')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroom')),
            ],
        ),
        migrations.AddField(
            model_name='mysteryroom',
            name='mystery_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroomcollection'),
        ),
        migrations.CreateModel(
            name='MRUserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(default=0)),
                ('submitted_answer', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('time_taken', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('mr_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroomcollection')),
                ('mr_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroomquestion')),
                ('mr_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysteryroom.mysteryroom')),
            ],
        ),
    ]
