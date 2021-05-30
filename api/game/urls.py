from django.urls import path

from .views import JoinGameView, LobbyView, PlayerView, GameView, GameResultView


urlpatterns = [
    path("join/", JoinGameView.as_view(), name="join-lobby"),
    path("lobby/<int:player_id>/", LobbyView.as_view(), name="get-lobby"),
    path("player/<int:player_id>/", PlayerView.as_view(), name="handle-player"),
    path(
        "game/<int:game_number>/<int:player_id>/",
        GameView.as_view(),
        name="handle-game",
    ),
    path(
        "result/<int:game_number>/", GameResultView.as_view(), name="handle-game-result"
    ),
]
