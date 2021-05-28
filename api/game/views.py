from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lobby, Player
from .serializers import JoinGameSerializer, LobbySerializer


class JoinGameView(APIView):
    """Handle requests related to lobby creation and lobby joining."""

    def post(self, request):

        join_serializer = JoinGameSerializer(data=request.data)
        if join_serializer.is_valid(raise_exception=True):
            lobby = Lobby.objects.filter(code__iexact=join_serializer.validated_data.get('code')).first()
            for player in lobby.players.all():
                if player.name == join_serializer.validated_data.get('name'):
                    return Response({"name": [f'Player with this name already exists in this lobby']}, status=status.HTTP_400_BAD_REQUEST)
            player = Player(name=join_serializer.validated_data.get('name'))
            player.lobby = lobby
            player.save()
            return Response({"detail": "super"}, status=status.HTTP_200_OK)


class LobbyView(APIView):
    """Handle requests related to user in lobby."""

    def get(self, request):
        pass

    