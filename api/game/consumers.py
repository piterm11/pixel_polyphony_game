import re
import json
import logging
from channels import Group
from channels.sessions import channel_session

from django.utils.timezone import now

from .models import Game


log = logging.getLogger("django")

# TODO change client, message and handle parameters


@channel_session
def ws_connect(message):
    # Extract the game from the message. This expects message.path to be of the
    # form /api/hit/{game_number}/, and finds a Game if the message path is applicable,
    # and if the Game exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        api, prefix, game_number = message["path"].decode("ascii").strip("/").split("/")
        if prefix != "hit" or api != "api":
            log.debug("invalid ws path=%s", message["path"])
            return
        game = Game.objects.get(id=game_number)
    except ValueError:
        log.debug("invalid ws path=%s", "None")
        return
    except Game.DoesNotExist:
        log.debug("ws game does not exist game_number=%s", game_number)
        return

    log.debug(
        "hit connect game=%s client=%s:%s",
        game.id,
        message["client"][0],
        message["client"][1],
    )

    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group("game-" + game.id, channel_layer=message.channel_layer).add(
        message.reply_channel
    )

    message.channel_session["game"] = game.id


@channel_session
def ws_receive(message):
    # Look up the game from the channel session, bailing if it doesn't exist
    try:
        game_number = message.channel_session["game"]
        game = Game.objects.get(id=game_number)
    except KeyError:
        log.debug("no game in channel_session")
        return
    except Game.DoesNotExist:
        log.debug(
            "recieved message, but game does not exist game_number=%s", game_number
        )
        return
    if game.date_end < now():
        log.debug(
            "received message, but game has already finished game_number=%s",
            game_number,
        )
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message["text"])
    except ValueError:
        log.debug("ws message isn't json text=%s", "None")
        return

    if set(data.keys()) != set(("handle", "message")):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug(
            "game message game=%s handle=%s message=%s",
            game.id,
            data["handle"],
            data["message"],
        )

        # hit = game.messages.create(**data)
        # check if game ended and perform proper operations

        # here create a new hit

        # See above for the note about Group
        Group("game-" + game_number, channel_layer=message.channel_layer).send(
            {"text": json.dumps(hit.as_dict())}
        )


@channel_session
def ws_disconnect(message):
    try:
        game_number = message.channel_session["game"]
        game = Game.objects.get(id=game_number)
        Group("game-" + game_number, channel_layer=message.channel_layer).discard(
            message.reply_channel
        )
    except (KeyError, Game.DoesNotExist):
        pass
