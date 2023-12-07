from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.chat_list, name='chat_list'),
    path('<int:room_id>/', views.chat_room, name='chat_room'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
]