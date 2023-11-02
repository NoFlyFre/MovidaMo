import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
from eventi.forms import AddEventForm
from raccomandazioni.models import Click
from utenti.views import profile_page
from .models import *
from movidamo.views import *
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from django.shortcuts import get_object_or_404
from eventi.models import Evento


def event_details(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    lat = str(evento.mappa_lat)
    long = str(evento.mappa_long)
    participating_users_number = len(Utente.objects.filter(
        utente_base__eventi_part=evento))
    showed_users = Utente.objects.filter(
        utente_base__eventi_part=evento).order_by('?')[:3]
    partial_partecipanti_number = participating_users_number - 3
    
    if request.user.is_authenticated and request.user.role == 'utente_base':
        Click.objects.create(user=request.user, event=evento, organizzatore=evento.get_organizzatore())
        # Recupera tutti gli amici dell'utente loggato
        user_friends = request.user.utente_base.amici.all()
        # Filtra gli amici che partecipano all'evento
        participating_friends = user_friends.filter(eventi_part=evento).exclude(pk=request.user.utente_base.pk)

        context = {
        'evento': evento, 
        'lat': lat, 
        'long': long,
        'n_partecipanti': participating_users_number, 
        'showed_users': showed_users, 
        'n_parziale_partecipanti': partial_partecipanti_number,
        'participating_friends': participating_friends
        }
    else:
        context = {
            'evento': evento, 
            'lat': lat, 
            'long': long,
            'n_partecipanti': participating_users_number, 
            'showed_users': showed_users, 
            'n_parziale_partecipanti': partial_partecipanti_number,
        }
    
    return render(request, '../templates/eventi/templates/dettagli_evento.html', context)


def search(request):
    eventi = Evento.objects.filter(nome__icontains=request.GET['search'])
    context = {'eventi': eventi}
    return render(request, 'eventi/search.html', context)


def filter_events(request):
    active_categories = request.GET.getlist('categories')

    if active_categories.__len__() == 0:
        events = Evento.objects.all().order_by('-id')
    else:
        events = Evento.objects.filter(
            categoria__id__in=active_categories).order_by('-id')

    categorie = Categoria.objects.all()
    has_today_events = events.filter(
        data=datetime.date.today()).exists()
    not_today_events = events.exclude(
        data__lte=datetime.date.today()).order_by('data')
    
    #Trasformare la lista di stringhe in una lista di interi
    active_categories = [int(i) for i in active_categories]
    
    #Filtrare gli eventi in base alla categoria
    if request.user.is_authenticated:
        recommended_events = get_recommended_events(request.user)
                        
        # Filtra gli eventi raccomandati per categoria
        if active_categories and len(recommended_events) > 0:
            filtered_events = [event for event in recommended_events if event.categoria.pk in active_categories]
        else:
            filtered_events = recommended_events
    else:
        filtered_events = []     
                
    context = {'title': "Trova la MOvida!", 'eventi': events,
               'not_today_events': not_today_events,
               "has_today_events": has_today_events, "categorie": categorie,
               "eventi_raccomandati": filtered_events, 'user': request.user}

    eventi = render_to_string('filtered_events_home.html', context=context)

    return JsonResponse({'events': eventi})


@user_passes_test(lambda u: u.is_authenticated and u.role == 'organizzatore', login_url='/')
def add_event(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            if form.is_valid():
                evento = form.save(commit=False)

                # Ottieni l'indirizzo dal form
                address = form.cleaned_data['address']

                # Effettua la richiesta all'API di geocoding di Mapbox
                response = requests.get(
                    f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json",
                    params={
                        'access_token': 'pk.eyJ1Ijoibm9mbHlmcmUiLCJhIjoiY2xoajYzenVkMGV3NzNkcDF2NWk5NTRpaiJ9.Mmpgnd70HuDK0Cc6LQnLwQ',
                        'limit': 1
                    }
                )

                # Estrai le coordinate geografiche dalla risposta JSON
                if response.status_code == 200:
                    data = response.json()
                    features = data.get('features')
                    if features:
                        coordinates = features[0].get(
                            'geometry', {}).get('coordinates')
                        if coordinates:
                            latitude = coordinates[1]
                            longitude = coordinates[0]

                            # Imposta le coordinate nel modello Evento
                            evento.mappa_lat = latitude
                            evento.mappa_long = longitude
                            
                    if form.cleaned_data['image'] is None:
                        image_path = os.path.join(settings.STATIC_ROOT, 'default_event.png')
                        with open(image_path, 'rb') as default_image:
                            evento.image.save('default_event.png', default_image, save=False)                
                
                evento.save()
                request.user.utente_organizzatore.eventi.add(evento)

                return redirect('profile_page', username=request.user.username)

    else:
        form = AddEventForm()

    context = {'form': form}
    return render(request, 'eventi/templates/add_event.html', context)


@login_required
def delete_event(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not is_organizzatore(request.user, evento):
        return redirect(home)

    evento.delete()
    return redirect(profile_page, username=request.user.username)


def is_organizzatore(user, evento):
    return user.role == 'organizzatore' and user.utente_organizzatore == evento.get_organizzatore()


@login_required
def edit_event(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not is_organizzatore(request.user, evento):
        # Reindirizza all'URL della home o alla view corrispondente
        return redirect(home)

    if request.method == 'POST':
        form = AddEventForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():

            address = form.cleaned_data['address']
            cap = form.cleaned_data['cap']

            response = requests.get(
                f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address} {cap} .json",
                params={
                    'access_token': 'pk.eyJ1Ijoibm9mbHlmcmUiLCJhIjoiY2xoajYzenVkMGV3NzNkcDF2NWk5NTRpaiJ9.Mmpgnd70HuDK0Cc6LQnLwQ',
                    'limit': 1,
                    'country': 'it',
                    'proximity': 'ip',
                    'language': 'it',
                }
            )
            
            # Estrai le coordinate geografiche dalla risposta JSON
            if response.status_code == 200:
                data = response.json()
                features = data.get('features')
                if features:
                    coordinates = features[0].get(
                        'geometry', {}).get('coordinates')
                    if coordinates:
                        latitude = coordinates[1]
                        longitude = coordinates[0]

                        # Imposta le coordinate nel modello Evento
                        evento.mappa_lat = latitude
                        evento.mappa_long = longitude
                        
                        evento.save()

            form.save()
            return redirect('profile_page', username=request.user.username)
        else:
            print(form.errors)
    else:
        data = evento.data.strftime('%Y-%m-%d')
        form = AddEventForm(instance=evento, initial={'data': data})

    context = {'form': form, 'evento_id': evento_id, 'evento': evento}
    return render(request, 'eventi/templates/edit_event.html', context)
