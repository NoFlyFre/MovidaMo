from django.shortcuts import render
from django.db.models import Count
import random
from eventi.models import *
from raccomandazioni.models import Click
from utenti.models import *
import datetime
import locale
from django.db.models import Q


# Imposta la localizzazione italiana
locale.setlocale(locale.LC_TIME, 'it_IT')


def home(request):
    eventi = Evento.objects.all().order_by('-id')
    has_today_events = Evento.objects.filter(
        data=datetime.date.today()).exists()
    categorie = Categoria.objects.all()
    not_today_events = eventi.exclude(
        data__lte=datetime.date.today()).order_by('data')

    if request.user.is_authenticated:
        recommended_events = get_recommended_events(request.user)
    else:
        recommended_events = []

    context = {'title': "Trova la MOvida!", 'eventi': eventi, "has_today_events": has_today_events,
               'not_today_events': not_today_events,
               "categorie": categorie,
               "eventi_raccomandati": recommended_events}

    return render(request, template_name='home.html', context=context)


def get_recommended_events(user):
    # Recupera le preferenze dell'utente basate sui dati dei click
    click_counts = Click.objects.filter(user=user).values(
        'event__categoria', 'event__organizzatore').annotate(count=Count('id'))
    
    total_click_counts = 0
    recommended_events = []
    
    # Calcola il numero totale di click   
    for click in click_counts:
        total_click_counts += click['count']
        
    if total_click_counts <= 50:
        return recommended_events
            
    # Crea un dizionario per memorizzare il conteggio dei click per categoria e organizzatore
    category_clicks = {}
    organizer_clicks = {}
    for click in click_counts:
        categoria = click['event__categoria']
        organizzatore = click['event__organizzatore']
        count = click['count']
        if categoria:
            category_clicks[categoria] = category_clicks.get(categoria, 0) + count
            
        if organizzatore:
            organizer_clicks[organizzatore] = organizer_clicks.get(organizzatore, 0) + count

    
    # Applica una soglia per determinare le categorie e gli organizzatori da considerare
    threshold = 0.25  # Soglia minima di click
 
    categories_to_consider = [categoria for categoria, count in category_clicks.items() if count/total_click_counts >= threshold]
    organizers_to_consider = [organizzatore for organizzatore, count in organizer_clicks.items() if count/total_click_counts >= threshold]
    
    # Recupera gli eventi futuri
    events = Evento.objects.filter(data__gte=datetime.date.today()).order_by('data')
    
    if categories_to_consider or organizers_to_consider:
        query = Q()
        if categories_to_consider:
            query |= Q(categoria__in=categories_to_consider)
        if organizers_to_consider:
            query |= Q(organizzatore__in=organizers_to_consider)
        events = events.filter(query)
    
    # Calcola il punteggio degli eventi basato sulle preferenze dell'utente
    scored_events = []
    for event in events:
        score = 0
        categoria = event.categoria
        organizzatore = event.get_organizzatore()
                                
        # Assegna un punteggio basato sui click dell'utente
        if categoria and categoria.pk in categories_to_consider:
            score += category_clicks[categoria.pk]
        if organizzatore and organizzatore.pk in organizers_to_consider:
            score += organizer_clicks[organizzatore.pk]
                    
        scored_events.append((event, score))

    
    # Ordina gli eventi in base al punteggio
    scored_events.sort(key=lambda x: x[1], reverse=True)

    # Mescola gli eventi con lo stesso punteggio
    grouped_events = []
    current_score = None
    current_group = []
    for event, score in scored_events:
        if score != current_score:
            if current_group:
                random.shuffle(current_group)
                grouped_events.extend(current_group)
            current_score = score
            current_group = [(event, score)]
        else:
            current_group.append((event, score))
        
    # Mescola l'ultimo gruppo
    if current_group:
        random.shuffle(current_group)
        grouped_events.extend(current_group)

    # Restituisci gli eventi raccomandati
    recommended_events = [event for event, _ in grouped_events]
        
    return recommended_events

