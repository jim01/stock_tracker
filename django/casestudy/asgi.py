import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from django.urls import re_path
from casestudy.consumers import WatchListConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'casestudy.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        URLRouter([
            re_path(r"ws/watchlist/(?P<user_id>\w+)/$", WatchListConsumer.as_asgi()),
            path("ws/watchlist/", WatchListConsumer.as_asgi()),
        ])
    ),
})

