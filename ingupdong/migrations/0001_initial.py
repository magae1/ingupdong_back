# Generated by Django 4.1.7 on 2023-02-27 23:44

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('handle', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'channel',
                'unique_together': {('name', 'handle')},
            },
        ),
        migrations.CreateModel(
            name='RecordingBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('time', models.TimeField(auto_now=True)),
            ],
            options={
                'db_table': 'recording',
                'ordering': ['-date', 'time'],
                'get_latest_by': ['date', 'time'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('url', models.CharField(max_length=50, unique=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel', to='ingupdong.channel')),
            ],
            options={
                'db_table': 'video',
            },
        ),
        migrations.CreateModel(
            name='TrendingBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField()),
                ('views', models.PositiveBigIntegerField()),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingupdong.recordingboard')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='ingupdong.video')),
            ],
            options={
                'db_table': 'trending',
                'ordering': ['record', 'rank'],
            },
            managers=[
                ('customs', django.db.models.manager.Manager()),
            ],
        ),
    ]
