from django.db import models
from django.db.models import fields
from game.models import Lobby
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Instrument, Lobby, Player


class JoinGameSerializer(ModelSerializer):
    """Serializer for join game view."""

    code = serializers.CharField(min_length=6, max_length=6, trim_whitespace=True)

    class Meta:
        model = Player
        fields = ['name', 'code']

    def validate_code(self, code):
        """Validate lobby code. Create a new lobby when there is no lobby assigned to code."""

        if not code.isalnum():
            raise ValidationError(["Code must be alphanumeric"])

        lobby = Lobby.objects.filter(code__iexact=code).first()

        if not lobby:
            lobby = Lobby(code=code.upper())
            lobby.save()
        if len(lobby.players.all()) > 4:
            raise ValidationError(["Lobby is full. Create a new one"])

        return code.upper()


class InstrumentSerializer(ModelSerializer):
    """Basic instrument serializer."""

    class Meta:
        model = Instrument
        fields = ['id', 'name']


class PlayerSerializer(ModelSerializer):
    """Basic player serializer."""

    instrument = InstrumentSerializer()

    class Meta:
        model = Player
        fields = ['name', 'want_play', 'instrument']

    # def update(self, instance, validated_data):
    #     print 'this - here'
    #     demo = Demo.objects.get(pk=instance.id)
    #     Demo.objects.filter(pk=instance.id)\
    #                        .update(**validated_data)
    #     return demo


class LobbyPlayerSerializer(ModelSerializer):
    """Serializer for player in lobby view."""

    code = serializers.SerializerMethodField()
    in_game = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    competitors = serializers.SerializerMethodField()
    available_instruments = serializers.SerializerMethodField()
    confirmed_players = serializers.SerializerMethodField()
    all_players = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['code', 'in_game', 'player', 'competitors',
            'available_instruments', 'confirmed_players', 'all_players']

# not sure if instance= is needed in serializers

    def get_code(self, player):
        return player.lobby.code

    def get_in_game(self, player):
        return player.lobby.in_game

    def get_player(self, player):
        return PlayerSerializer(player).data

    def get_competitors(self, player):
        lobby = player.lobby
        competitors = list(lobby.players.all())
        competitors.remove(player)
        return PlayerSerializer(competitors, many=True).data

    def get_available_instruments(self, player):
        available_instruments = list(Instrument.objects.all())
        lobby = player.lobby
        for player in lobby.players.all():
            if player.instrument in available_instruments:
                available_instruments.remove(player.instrument)
        return InstrumentSerializer(available_instruments, many=True).data

    def get_confirmed_players(self, player):
        lobby = player.lobby
        return len(lobby.players.filter(want_play=True).all())

    def get_all_players(self, player):
        lobby = player.lobby
        return len(lobby.players.all())
