from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    # URL per la chat WebSocket
    path('ws/chat/<int:room_id>/', consumers.ChatConsumer.as_asgi()), 
]
