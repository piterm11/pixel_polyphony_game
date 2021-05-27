# Generated by Django 3.2.3 on 2021-05-27 12:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import game.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(auto_now_add=True)),
                ('date_end', models.DateTimeField(default=game.utils.create_end_game_datetime)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=game.utils.create_short_uuid, max_length=6, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('in_game', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6, unique=True)),
                ('value', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('want_play', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.instrument')),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.lobby')),
            ],
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hit_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.game')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.instrument')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.player')),
                ('tone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.tone')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='lobby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.lobby'),
        ),
    ]
