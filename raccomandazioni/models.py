from django.db import models
from utenti.models import Utente, Organizzatore
from eventi.models import Evento


class Click(models.Model):
    user = models.ForeignKey(Utente, on_delete=models.CASCADE)
    event = models.ForeignKey(Evento, on_delete=models.CASCADE)
    organizzatore = models.ForeignKey(Organizzatore, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp) + ' - ' + self.user.username + " - " + self.event.name + " - " + self.organizzatore.nome
    
    
