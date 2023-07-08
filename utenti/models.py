from django.contrib.auth.models import AbstractUser
from django.db import models


class Utente(AbstractUser):
    class Role(models.TextChoices):
        ORGANIZZATORE = 'organizzatore', 'Organizzatore'
        UTENTE_BASE = 'utente_base', 'Utente Base'
        ADMIN = 'admin', 'Admin'

    base_role = Role.UTENTE_BASE
    role = models.CharField('Role', max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.role + " - " + self.username

    class Meta:
        verbose_name_plural = "Utenti"


class Organizzatore(models.Model):
    utente = models.OneToOneField(
        Utente, on_delete=models.CASCADE, related_name='utente_organizzatore', primary_key=True)
    nome = models.CharField(max_length=255)
    img = models.ImageField(upload_to='organizzatori/')
    cover_img = models.ImageField(upload_to='organizzatori/', blank=True)
    eventi = models.ManyToManyField('eventi.Evento')

    base_role = Utente.Role.ORGANIZZATORE

    def __str__(self):
        return self.utente.username
    
    class Meta:
        verbose_name_plural = "Organizzatori"



class UtenteBase(models.Model):
    utente = models.OneToOneField(
        Utente, on_delete=models.CASCADE, related_name='utente_base', primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    interests = models.ManyToManyField('eventi.Categoria', blank=True)
    img = models.ImageField(upload_to='utenti/', blank=True, null=True)
    cover_img = models.ImageField(upload_to='utenti/', blank=True, null=True)
    eventi_part = models.ManyToManyField('eventi.Evento', blank=True)
    private_future_events = models.BooleanField(default=False)
    
    def __str__(self):
        return self.utente.username
    
    class Meta:
        verbose_name_plural = "Utenti Base"
        
        

