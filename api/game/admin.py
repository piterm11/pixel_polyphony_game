from django.contrib import admin

from .models import Lobby, Player, Instrument, Game, Hit


admin.site.register(Lobby)
admin.site.register(Player)
admin.site.register(Instrument)
admin.site.register(Game)
admin.site.register(Hit)
