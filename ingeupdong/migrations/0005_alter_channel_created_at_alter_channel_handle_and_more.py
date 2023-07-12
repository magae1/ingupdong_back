# Generated by Django 4.1.9 on 2023-07-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingeupdong', '0004_alter_trendingboard_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='채널의 첫 크롤링 날짜'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='handle',
            field=models.CharField(help_text='채널 핸들명', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(help_text='채널명', max_length=150),
        ),
        migrations.AlterField(
            model_name='recordingboard',
            name='record_at',
            field=models.DateTimeField(auto_now=True, help_text='크롤링 날짜'),
        ),
        migrations.AlterField(
            model_name='trendingboard',
            name='rank',
            field=models.PositiveSmallIntegerField(help_text='인급동 순위'),
        ),
        migrations.AlterField(
            model_name='trendingboard',
            name='views',
            field=models.PositiveBigIntegerField(help_text='영상 조회수'),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='영상의 첫 크롤링 날짜'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(help_text='동영상 제목', max_length=120),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(help_text='동영상 url', max_length=50, unique=True),
        ),
    ]
