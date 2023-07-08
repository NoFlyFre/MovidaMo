from django.contrib import admin
from eventi.models import Evento, Categoria
from raccomandazioni.models import Click
from utenti.models import *

admin.site.register(Evento)
admin.site.register(Categoria)
admin.site.register(Utente)
admin.site.register(Organizzatore)
admin.site.register(UtenteBase)
admin.site.register(Click)