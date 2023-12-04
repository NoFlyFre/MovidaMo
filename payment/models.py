from django.db import models
from utenti.models import Utente
from eventi.models import Evento

class Ticket(models.Model):
    user = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Evento, on_delete=models.CASCADE)  # Sostituisci 'EventModel' con il nome effettivo del tuo modello evento
    qr_code = models.ImageField(upload_to='tickets_qr/', null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket for {self.event.name} - User: {self.user.username}"

class Transaction(models.Model):
    user = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='transactions')
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)  # ID transazione da Stripe
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.event.name} - {self.amount} - {self.user.username}"