from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import re_path
from channels.auth import AuthMiddlewareStack

from . import consummers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_id>\w+)/$', consummers.GameConsummer)
]