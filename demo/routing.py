from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("message/error", consumers.MessageConsumer.as_asgi()),
    re_path("view/data", consumers.SingleConsumer.as_asgi()),
]
