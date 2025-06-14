# groups/routing.py
from django.urls import re_path

from payments import consumers

websocket_urlpatterns = [
    re_path(r'ws/payouts/(?P<group_id>\w+)/$', consumers.PayoutConsumer.as_asgi()),
]