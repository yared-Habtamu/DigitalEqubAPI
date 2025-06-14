from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import groups.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        groups.routing.websocket_urlpatterns
    ),
})