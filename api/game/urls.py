from django.urls import path

from .views import JoinGameView, LobbyView


urlpatterns = [
    path('join/', JoinGameView.as_view(), name='join-lobby'),
    path('lobby/<int:player_id>/', LobbyView.as_view(), name='get-lobby'),
]