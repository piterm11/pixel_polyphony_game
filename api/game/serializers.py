from django.core.exceptions import ValidationError
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from game.models import Game, Hit, Instrument, Lobby, Player


class JoinGameSerializer(ModelSerializer):
    """Serializer for join game view."""

    code = serializers.CharField(min_length=6, max_length=6, trim_whitespace=True)

    class Meta:
        model = Player
        fields = ["name", "code"]

    def validate_code(self, code):
        """Validate lobby code. Create a new lobby when there is no lobby assigned to code."""

        if not code.isalnum():
            raise ValidationError(["Code must be alphanumeric"])

        lobby = Lobby.objects.filter(code__iexact=code).first()

        if not lobby:
            lobby = Lobby(code=code.upper())
            lobby.save()
        if len(lobby.players.filter(active=True).all()) > 4:
            raise ValidationError(["Lobby is full. Create a new one"])

        return code.upper()


class InstrumentSerializer(ModelSerializer):
    """Basic instrument serializer."""

    class Meta:
        model = Instrument
        fields = ["id", "name"]


class ShowPlayerSerializer(ModelSerializer):
    """Show player serializer."""

    class Meta:
        model = Player
        fields = ["id", "name", "want_play", "instrument"]

    def to_representation(self, instance):
        rep = super(ShowPlayerSerializer, self).to_representation(instance)
        if instance.instrument:
            rep["instrument"] = instance.instrument.name
        return rep


class UpdatePlayerSerializer(serializers.Serializer):
    """Update player serializer."""

    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=60)
    want_play = serializers.BooleanField()
    instrument = serializers.CharField(allow_null=True)

    def validate_instrument(self, instrument):
        if instrument:
            instrument_in_db = Instrument.objects.filter(
                name__iexact=instrument
            ).first()
            if not instrument_in_db:
                raise ValidationError(["Invalid instrument name passed"])
            return instrument_in_db
        return instrument


class LobbyPlayerSerializer(ModelSerializer):
    """Serializer for player in lobby view."""

    code = serializers.SerializerMethodField()
    game_number = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    available_instruments = serializers.SerializerMethodField()
    confirmed_players = serializers.SerializerMethodField()
    all_players = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            "code",
            "game_number",
            "player",
            "team",
            "available_instruments",
            "confirmed_players",
            "all_players",
        ]

    def get_code(self, player):
        return player.lobby.code

    def get_game_number(self, player):
        return player.lobby.game_number

    def get_player(self, player):
        return ShowPlayerSerializer(player).data

    def get_team(self, player):
        lobby = player.lobby
        team = list(lobby.players.filter(active=True).all())
        team.remove(player)
        return ShowPlayerSerializer(team, many=True).data

    def get_available_instruments(self, player):
        available_instruments = list(Instrument.objects.all())
        lobby = player.lobby
        for player in lobby.players.filter(active=True).all():
            if player.instrument in available_instruments:
                available_instruments.remove(player.instrument)
        return [instrument.name for instrument in available_instruments]

    def get_confirmed_players(self, player):
        lobby = player.lobby
        return len(lobby.players.filter(want_play=True, active=True).all())

    def get_all_players(self, player):
        lobby = player.lobby
        return len(lobby.players.filter(active=True).all())


class ShowGamePlayerSerializer(ModelSerializer):
    """Serializer for player game view."""

    game_number = serializers.SerializerMethodField()
    date_start = serializers.SerializerMethodField()
    date_end = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ["game_number", "date_start", "date_end", "player", "team"]

    def get_game_number(self, player):
        return player.lobby.game_number

    def get_date_start(self, player):
        return (
            player.lobby.games.filter(date_end__gt=now()).first().date_start.isoformat()
        )

    def get_date_end(self, player):
        return (
            player.lobby.games.filter(date_end__gt=now()).first().date_end.isoformat()
        )

    def get_player(self, player):
        return ShowPlayerSerializer(player).data

    def get_team(self, player):
        lobby = player.lobby
        team = list(lobby.players.filter(active=True).all())
        team.remove(player)
        return ShowPlayerSerializer(team, many=True).data


# TODO
# when someone will want to check the result later e.g. when team
# is preparing to the next game
# incorrect players and isntruments can be displayed
# needed another relation for game players
class ShowGameResultSerializer(ModelSerializer):
    """Serializer for game result view."""

    game_number = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["game_number", "date_start", "date_end", "players", "result"]

    def get_game_number(self, game):
        return game.id

    def get_players(self, game):
        lobby = game.lobby
        team = list(lobby.players.filter(active=True).all())
        return ShowPlayerSerializer(team, many=True).data

    def get_result(self, game):
        return game.result
