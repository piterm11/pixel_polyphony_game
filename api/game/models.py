from django.db import models
from django.db.models.deletion import PROTECT
from django.utils.timezone import now

from .utils import create_end_game_datetime, create_short_uuid

# user types code, but must be validated and trimmed
# validate if uuid passed is 6 length
class Lobby(models.Model):
    code = models.CharField(max_length=6, unique=True, default=create_short_uuid)
    creation_date = models.DateTimeField(auto_now_add=True)
    in_game = models.BooleanField(default=False)

class Instrument(models.Model):
    name = models.CharField(max_length=60)

# use exclude active=False when counting the number of connected users
class Player(models.Model):
    name = models.CharField(max_length=60, unique=False)
    join_date = models.DateTimeField(auto_now_add=True)
    want_play = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    lobby = models.ForeignKey(Lobby, on_delete=models.PROTECT)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)

class Game(models.Model):
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(default=create_end_game_datetime)
    lobby = models.ForeignKey(Lobby, on_delete=models.PROTECT)
    #players = models.ManyToManyField(Player, related_name='games')

class Tone(models.Model):
    name = models.CharField(max_length=6, unique=True)
    value = models.PositiveSmallIntegerField()

class Hit(models.Model):
    hit_date = models.DateTimeField(default=now)
    player = models.ForeignKey(Player, on_delete=PROTECT)
    instrument = models.ForeignKey(Instrument, on_delete=PROTECT)
    tone = models.ForeignKey(Tone, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
