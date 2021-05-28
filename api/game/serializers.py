from django.db.models import fields
from game.models import Lobby
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Lobby, Player


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


class PlayerSerializer(ModelSerializer):

    class Meta:
        model = Player
        fields = ['name', 'want_play', 'instrument']


class LobbySerializer(ModelSerializer):


    class Meta:
        model = Lobby
        fields = ["code",]