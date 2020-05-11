from django.urls import re_path

from .ws_consurmers import ChatroomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<room_name>\w+)/$', ChatroomConsumer),
]