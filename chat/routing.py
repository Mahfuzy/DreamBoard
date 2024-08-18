from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/direct/<str:username>/', consumers.DirectChatConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', consumers.GroupChatConsumer.as_asgi()),
]
