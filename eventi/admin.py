import random
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from .models import Evento, Categoria  # Assicurati di importare i tuoi modelli

def set_events_to_today(modeladmin, request, queryset):
    queryset.update(data=timezone.now().date())

def set_events_to_future(modeladmin, request, queryset):
    for event in queryset:
        random_days = random.randint(1, 14)  # Genera un numero casuale tra 1 e 14
        future_date = timezone.now().date() + timedelta(days=random_days)
        event.data = future_date
        event.save()  # Non dimenticare di salvare l'evento dopo aver modificato la data

set_events_to_today.short_description = "Imposta gli eventi alla data odierna"
set_events_to_future.short_description = "Imposta gli eventi ad una data futura"

@admin.register(Evento)
class EventAdmin(admin.ModelAdmin):
    list_display = ['data','name', 'categoria']
    actions = [set_events_to_today, set_events_to_future]

admin.site.register(Categoria)
