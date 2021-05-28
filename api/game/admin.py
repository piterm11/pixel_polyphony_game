from django.contrib import admin

from .models import Lobby, Player, Instrument, Game, Tone, Hit


admin.site.register(Lobby)
admin.site.register(Player)
admin.site.register(Instrument)
admin.site.register(Game)
admin.site.register(Tone)
admin.site.register(Hit)
