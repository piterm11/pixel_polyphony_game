# import os

# from channels.layers import get_channel_layer


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# channel_layer = get_channel_layer()

# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# django.setup()
# application = get_default_application()



# TODO check regex

import django
django.setup()

import os

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from game.consumers import HitConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url(r"^api/hit/(?P<game_number>[0-9]+)/$", HitConsumer),
            ])
        ),
    ),
})
