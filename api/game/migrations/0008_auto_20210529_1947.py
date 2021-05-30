# Generated by Django 3.2.3 on 2021-05-29 19:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_game_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='player',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]