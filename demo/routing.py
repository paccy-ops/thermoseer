from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer
from .views import view
from . import consumers


websocket_urlpatterns = [
    re_path(r"^ws/$", consumers.PostConsumer.as_asgi()),
    re_path("view/data", consumers.SingleConsumer.as_asgi()),
]
