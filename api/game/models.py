from django.db import models
from django.db.models.deletion import PROTECT
from django.utils.timezone import now

from .utils import (
    create_end_game_datetime,
    create_start_game_datetime,
    create_short_uuid,
)


class Lobby(models.Model):
    code = models.CharField(max_length=6, unique=True, default=create_short_uuid)
    creation_date = models.DateTimeField(default=now)
    game_number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.code


class Instrument(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=60, unique=False)
    join_date = models.DateTimeField(default=now)
    want_play = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    lobby = models.ForeignKey(Lobby, on_delete=models.PROTECT, related_name="players")
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="players",
    )

    def __str__(self):
        return f"{self.name} {self.lobby}"


class Game(models.Model):
    date_start = models.DateTimeField(default=create_start_game_datetime)
    date_end = models.DateTimeField(default=create_end_game_datetime)
    result = models.JSONField(null=True)
    lobby = models.ForeignKey(Lobby, on_delete=models.PROTECT, related_name="games")

    def __str__(self):
        return f"{self.id} {self.lobby}"

class Hit(models.Model):
    hit_date = models.DateTimeField(default=now)
    instrument = models.ForeignKey(Instrument, on_delete=PROTECT, related_name="hits")
    tone = models.CharField(max_length=1, default="A")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="hits")

    def __str__(self):
        return f"{self.tone} {self.game}"
