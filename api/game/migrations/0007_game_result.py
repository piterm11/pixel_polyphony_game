# Generated by Django 3.2.3 on 2021-05-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20210528_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='result',
            field=models.JSONField(null=True),
        ),
    ]
