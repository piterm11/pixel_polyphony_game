# Generated by Django 3.2.3 on 2021-05-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_instrument_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lobby',
            name='in_game',
        ),
        migrations.AddField(
            model_name='lobby',
            name='game_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
