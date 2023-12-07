from django.db import models
from django.conf import settings
from utenti.models import Utente

class ChatRoom(models.Model):
    participante1 = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="chat_participant1")
    participante2 = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="chat_participant2")

    def __str__(self):
        return f"{self.participante1.username} - {self.participante2.username}"
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Utente, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    evento = models.ForeignKey('eventi.Evento', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.room.id}"

