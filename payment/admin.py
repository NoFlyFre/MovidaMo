from django.contrib import admin
from .models import Ticket, Transaction

admin.site.register(Ticket)
admin.site.register(Transaction)