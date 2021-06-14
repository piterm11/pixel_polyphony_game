import json
import logging

# from channels import Group
# from channels.sessions import channel_session

from django.utils.timezone import now

from .models import Game, Instrument, Hit


log = logging.getLogger("django")


# @channel_session
# def ws_connect(message):
#     # Extract the game from the message. This expects message.path to be of the
#     # form /api/hit/{game_number}/, and finds a Game if the message path is applicable,
#     # and if the Game exists. Otherwise, bails (meaning this is a some othersort
#     # of websocket). So, this is effectively a version of _get_object_or_404.

#     try:
#         api, prefix, game_number = message["path"].decode("ascii").strip("/").split("/")
#         if prefix != "hit" or api != "api":
#             log.debug("invalid ws path=%s", message["path"])
#             return
#         game = Game.objects.get(id=game_number)
#     except ValueError:
#         log.debug("invalid ws path=%s", "None")
#         return
#     except Game.DoesNotExist:
#         log.debug("ws game does not exist game_number=%s", game_number)
#         return

#     log.debug(
#         "hit connect game=%s client=%s:%s",
#         game.id,
#         message["client"][0],
#         message["client"][1],
#     )

#     # Need to be explicit about the channel layer so that testability works
#     # This may be a FIXME?
#     Group("game-" + game.id, channel_layer=message.channel_layer).add(
#         message.reply_channel
#     )

#     message.channel_session["game"] = game.id


# @channel_session
# def ws_receive(message):
#     # Look up the game from the channel session, bailing if it doesn't exist
#     try:
#         game_number = message.channel_session["game"]
#         game = Game.objects.get(id=game_number)
#     except KeyError:
#         log.debug("no game in channel_session")
#         return
#     except Game.DoesNotExist:
#         log.debug(
#             "recieved message, but game does not exist game_number=%s", game_number
#         )
#         return
#     if game.date_end < now():
#         log.debug(
#             "received message, but game has already finished game_number=%s",
#             game_number,
#         )
#         return

#     # Parse out a chat message from the content text, bailing if it doesn't
#     # conform to the expected message format.
#     try:
#         data = json.loads(message["text"])
#     except ValueError:
#         log.debug("ws message isn't json text=%s", "None")
#         return

#     if set(data.keys()) != set(("handle", "message")):
#         log.debug("ws message unexpected format data=%s", data)
#         return

#     if data:
#         log.debug(
#             "game message game=%s handle=%s message=%s",
#             game.id,
#             data["handle"],
#             data["message"],
#         )

#         # hit = game.messages.create(**data)
#         # check if game ended and perform proper operations

#         # here create a new hit

#         # See above for the note about Group
#         Group("game-" + game_number, channel_layer=message.channel_layer).send(
#             {"text": json.dumps(hit.as_dict())}
#         )


# @channel_session
# def ws_disconnect(message):
#     try:
#         game_number = message.channel_session["game"]
#         game = Game.objects.get(id=game_number)
#         Group("game-" + game_number, channel_layer=message.channel_layer).discard(
#             message.reply_channel
#         )
#     except (AsyncConsumer):
#         pass


# TODO do we need await call with logger? Do we need to add sync_to_async?
# TODO mesage sent to the ended game does not create a game result song.

from asgiref.sync import sync_to_async

from channels.consumer import AsyncConsumer, StopConsumer
from channels.db import database_sync_to_async


class HitConsumer(AsyncConsumer):

    AVAILABLE_TONES = ["c", "D", "E", "F", "G", "A", "H", "C"]

    async def websocket_connect(self, event):
        """Connect new player to the proper group or create a new websocket group."""

        print("connected", event)

        try:
            game_number = int(self.scope["url_route"]["kwargs"]["game_number"])
        except (KeyError, ValueError):
            await self.log_error("Invalid or missing game number")
            return
        try:
            game = Game.objects.get(id=game_number)
        except Game.DoesNotExist:
            await self.log_error(
                f"received message, but game does not exist game_number={game_number}"
            )
            return
        if game.date_end < now():
            await self.log_error("Game ended already")
            return
        game_name = f"game-{game_number}"
        self.game_room = game_name
        self.game_number = game_number
        self.channel_layer.group_add(game_name, self.channel_name)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )
        await self.log_error(
            f"New websocket player connected to the game '{game_name}'"
        )

    async def websocket_receive(self, event):
        """Handle message sent by player and propagate the all players in websocket group."""
        print("receive", event)

        data = event.get("text", None)
        if not data:
            await self.log_error("No data in the message")
            return
        data = json.loads(data)
        instrument_name = data.get("instrument")
        tone = data.get("tone")
        if not instrument_name:
            await self.log_error("Missing argument 'instrument' in the message")
            return
        if not tone:
            await self.log_error("Missing argument 'tone' in the message")
            return
        hit = await self.add_hit(instrument_name, tone)
        if not hit:
            await self.log_error(
                "Cannot save the hit. Game ended or invalid message was sent."
            )
            return

        new_message = {
            "type": "game_message",
            "text": json.dumps({"instrument": instrument_name, "tone": tone}),
        }

        # broadcast the event message
        await self.channel_layer.group_send(self.game_room, new_message)

    async def game_message(self, event):
        """Send message with hit info."""
        # send the actual message
        await self.send({"type": "websocket.send", "text": event["text"]})

    @database_sync_to_async
    def add_hit(self, instrument_name, tone):
        """Add new game hit asynchronously."""
        instrument = Instrument.objects.filter(name__iexact=instrument_name).first()
        if not instrument:
            return None
        game = Game.objects.filter(id=self.game_number).first()
        if not game or game.date_end < now():
            return None
        if tone.upper() not in self.AVAILABLE_TONES:
            return None
        return Hit.objects.create(tone=tone, instrument=instrument, game=game)

    @sync_to_async
    def log_error(self, message):
        """Log errors and info asynchronously."""
        log.debug(message)

    async def websocket_disconnect(self, event):
        """Close player websocket connection."""
        print("disconnected", event)
        raise StopConsumer()
