from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Lobby, Player
from .serializers import (
    JoinGameSerializer,
    LobbyPlayerSerializer,
    ShowPlayerSerializer,
    UpdatePlayerSerializer,
)


class JoinGameView(APIView):
    """Handle requests related to lobby creation and lobby joining."""

    def post(self, request):
        join_serializer = JoinGameSerializer(data=request.data)
        if join_serializer.is_valid(raise_exception=True):
            lobby = Lobby.objects.filter(
                code__iexact=join_serializer.validated_data.get("code")
            ).first()
            for player in lobby.players.all():
                if player.name == join_serializer.validated_data.get("name"):
                    return Response(
                        {
                            "name": [
                                f"Player with this name already exists in this lobby"
                            ]
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            player = Player(name=join_serializer.validated_data.get("name"))
            player.lobby = lobby
            player.save()
            return Response(
                LobbyPlayerSerializer(player).data, status=status.HTTP_200_OK
            )


class LobbyView(APIView):
    """Handle requests related to player in lobby."""

    def get(self, request, player_id):
        player = Player.objects.filter(id=player_id, active=True).first()
        if not player:
            return Response(
                {"detail": [f"No player with this id"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(LobbyPlayerSerializer(player).data, status=status.HTTP_200_OK)


class PlayerView(APIView):
    """Handle requests related to player state."""

    def get(self, request, player_id):
        player = Player.objects.filter(id=player_id, active=True).first()
        if not player:
            return Response(
                {"detail": [f"No player with this id"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.check_end_game(player)
        if player.lobby.game_number:
            return Response(
                {"detail": [f"Lobby in game. Try later"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(ShowPlayerSerializer(player).data, status=status.HTTP_200_OK)

    def put(self, request, player_id):
        player = Player.objects.filter(id=player_id, active=True).first()
        if not player:
            return Response(
                {"detail": [f"No player with this id"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.check_end_game(player)
        if player.lobby.game_number:
            return Response(
                {"detail": [f"Lobby in game. Try later"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UpdatePlayerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if player.id != serializer.validated_data.get("id"):
                return Response(
                    {"detail": [f"Not matching player ids passed"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instrument = serializer.validated_data.get("instrument")
            if instrument:
                if (
                    player.lobby.players.exclude(name=player.name)
                    .filter(instrument=instrument, active=True)
                    .first()
                ):
                    return Response(
                        {"detail": [f"Instrument is already used in this lobby"]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            player.instrument = instrument
            name = serializer.validated_data.get("name")
            if (
                player.lobby.players.exclude(id=player.id)
                .filter(name=name, active=True)
                .first()
            ):
                return Response(
                    {"detail": [f"Player with this name already exists in this lobby"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            player.name = name
            player.want_play = serializer.validated_data.get("want_play")
            player.save()
            if player.want_play:
                self.check_run_game(player)
            return Response(
                ShowPlayerSerializer(player).data, status=status.HTTP_200_OK
            )

    def delete(self, request, player_id):
        player = Player.objects.filter(id=player_id, active=True).first()
        if not player:
            return Response(
                {"detail": [f"No player with this id"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.check_end_game(player)
        if player.lobby.game_number:
            return Response(
                {"detail": [f"Lobby in game. Try later"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        player.active = False
        player.save()
        return Response(
            {"detail": "Player deleted successfully"}, status=status.HTTP_200_OK
        )

    def check_run_game(self, player):
        """Check if all players are ready and run a new game."""
        if not player.lobby.players.filter(want_play=False, active=True).first():
            game = Game(lobby=player.lobby)
            game.save()
            player.lobby.game_number = game.id
            player.lobby.save()

    def check_end_game(self, player):
        """Check if current game ended and prepare players for a new round."""
        if player.lobby.game_number:
            if not Game.objects.filter(
                id=player.lobby.game_number, date_end__gt=now()
            ).first():
                player.lobby.game_number = None
                player.lobby.save()
                for player in player.lobby.players.filter(active=True).all():
                    player.instrument = None
                    player.want_play = False
                    player.save()
