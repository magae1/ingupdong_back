# Generated by Django 4.1.9 on 2023-07-15 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingeupdong', '0005_alter_channel_created_at_alter_channel_handle_and_more'),
        ('rank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoringboard',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='ingeupdong.channel'),
        ),
    ]