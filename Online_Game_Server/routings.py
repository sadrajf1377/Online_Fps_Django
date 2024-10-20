from django.urls import re_path
from .consumers import Private_Socket,Room_Socket,Web_Consumer,Group_Socket
websocket_urlpatterns = [
re_path(r"ws/private_socekt/(?P<username>\w+)/$",Private_Socket.as_asgi()),
re_path(r"ws/room/(?P<room_name>\w+)/$",Room_Socket.as_asgi())
    ,re_path(r"ws/web_socekt/(?P<room_name>\w+)/$",Web_Consumer.as_asgi())
    , re_path(r"ws/group_socket/(?P<room_name>\w+)/$", Group_Socket.as_asgi())
]