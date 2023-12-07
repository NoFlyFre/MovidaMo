# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    
    connected_users = {}  # Dizionario per tenere traccia degli utenti connessi in ogni stanza di chat

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_id']

        # Aggiungi l'utente alla stanza per tenere traccia degli utenti connessi
        ChatConsumer.connected_users[self.room_name] = ChatConsumer.connected_users.get(self.room_name, set())
        ChatConsumer.connected_users[self.room_name].add(self.user)

        # Verifica se l'utente è autenticato prima di accettare la connessione
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_group_name = f'chat_{self.room_name}'

            # Aggiungi questo socket alla chat group per inviare/ricevere messaggi
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accetta la connessione WebSocket
            await self.accept()

    async def disconnect(self, close_code):
        # Rimuovi l'utente dalla stanza alla disconnessione
        ChatConsumer.connected_users[self.room_name].discard(self.user)
        if len(ChatConsumer.connected_users[self.room_name]) == 0:
            del ChatConsumer.connected_users[self.room_name]

        # Rimuovi il socket dalla chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope["user"]

        # Ottieni l'URL dell'immagine del mittente
        sender_image_url = await self.get_user_image_url(sender)

        # Inoltra il messaggio al gruppo della chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'sender_image_url': sender_image_url,
            }
        )

        # Salva il messaggio nel database
        await self.save_message(message)

    async def chat_message(self, event):
        # Metodo helper per gestire l'invio di messaggi al WebSocket client
        message = event['message']
        sender = event['sender']
        sender_image_url = event['sender_image_url']

        # Invia il messaggio al WebSocket client, includendo l'URL dell'immagine dell'altro utente
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_image_url': sender_image_url,
        }))

    @database_sync_to_async
    def get_chat_room(self, room_id):
        try:
            return ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return None


    @database_sync_to_async
    def get_other_user(self, chat_room, current_user):
        if chat_room.participante1 == current_user:
            return chat_room.participante2
        else:
            return chat_room.participante1


    @database_sync_to_async
    def get_user_image_url(self, user):
        if hasattr(user, 'utente_organizzatore'):
            return user.utente_organizzatore.img.url if user.utente_organizzatore.img else None
        elif hasattr(user, 'utente_base'):
            return user.utente_base.img.url if user.utente_base.img else None
        return None


    @database_sync_to_async
    def save_message(self, message):
        # Salva il messaggio nel database e imposta lo stato di lettura
        is_read = self.check_if_user_is_in_same_room()

        Message.objects.create(
            room_id=self.room_name,
            sender=self.scope["user"],
            message=message,
            is_read=is_read
        )

    def check_if_user_is_in_same_room(self):
        # Controlla se l'altro partecipante della chat è attualmente connesso alla stessa stanza
        users_in_room = ChatConsumer.connected_users.get(self.room_name, set())
        return any(user != self.user for user in users_in_room)
