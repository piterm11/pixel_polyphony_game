from django.urls import path

from .views import JoinGameView, LobbyView, PlayerView


urlpatterns = [
    path("join/", JoinGameView.as_view(), name="join-lobby"),
    path("lobby/<int:player_id>/", LobbyView.as_view(), name="get-lobby"),
    path("player/<int:player_id>/", PlayerView.as_view(), name="handle-player"),
]
