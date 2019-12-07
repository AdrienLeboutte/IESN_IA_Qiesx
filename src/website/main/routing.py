from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import re_path
from django.urls import path
from channels.auth import AuthMiddlewareStack

from . import consummers

websocket_urlpatterns = [
    path('ws/game/<str:game_id>/', consummers.GameConsummer)
]