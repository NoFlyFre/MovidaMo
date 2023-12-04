from django.shortcuts import render
from django.utils import timezone
from payment.models import Ticket
from payment.views import create_stripe_account
from utenti.forms import OrganizzatoreProfileEditForm, OrganizzatoreSignUpForm, UserProfileEditForm, UtenteSignUpForm, UtenteLoginForm
from utenti.models import Utente
from utenti.models import UtenteBase
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from movidamo.views import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notifica
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def register_request(request):
    if request.method == "POST":
        form = UtenteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(edit_profile, username=request.user.username)
    else:
        form = UtenteSignUpForm()

    return render(request=request, template_name="utenti/templates/signup_user.html", context={"form": form})


def register_request_organizer(request):
    if request.method == "POST":
        form = OrganizzatoreSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Registration successful.")
            redirect_url = create_stripe_account(request)
            return HttpResponseRedirect(redirect_url)
        
    else:
        form = OrganizzatoreSignUpForm()

    return render(request=request, template_name="utenti/templates/signup_organizer.html", context={"form": form})


def logout_request(request):
    logout(request)
    return redirect('../login')


def login_request(request):
    if request.method == "POST":
        form = UtenteLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect(home)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UtenteLoginForm(request)

    return render(request, "utenti/templates/login_user.html", {"form": form})


def profile_page(request, username):
    utente = Utente.objects.get(username=username)
    friend_request_status = 0
    
    # Eventi
    if utente.role == Utente.Role.ORGANIZZATORE:
        tot_events = utente.utente_organizzatore.eventi.count()
        eventi_passati = utente.utente_organizzatore.eventi.filter(
            data__lt=timezone.now()).order_by('-data')
        eventi_futuri = utente.utente_organizzatore.eventi.filter(
            data__gte=timezone.now()).order_by('data')
        
        context = {
        'profile_user': utente,
        'eventi_pass': eventi_passati,
        'eventi_fut': eventi_futuri,
        'tot_events': tot_events
        }

    else:
        tot_events = utente.utente_base.eventi_part.count()
        eventi_passati = utente.utente_base.eventi_part.filter(
            data__lt=timezone.now()).order_by('-data')
        eventi_futuri = utente.utente_base.eventi_part.filter(
            data__gte=timezone.now()).order_by('data')
        n_friends = utente.utente_base.amici.count()
        print(n_friends)
    
        # Verifica dello stato della richiesta di amicizia
        if request.user.is_authenticated:
            mittente = request.user
            # Verifica se esiste una notifica di richiesta di amicizia
            notifica = Notifica.objects.filter(
                mittente=mittente,
                user=utente,
                tipo=Notifica.RICHIESTA_AMICIZIA
            ).first()
            
            friends = utente.utente_base in mittente.utente_base.amici.all()
            
            # Se la notifica non esiste
            if not notifica and friends:
                friend_request_status = 2
            # Se gli utenti sono amici
            elif notifica:
                friend_request_status = 1
            elif not notifica:
                friend_request_status = 0
                

        context = {
            'profile_user': utente,
            'eventi_pass': eventi_passati,
            'eventi_fut': eventi_futuri,
            'tot_events': tot_events,
            'friend_request_status': friend_request_status,
            'friends_number': n_friends,
        }
        

    return render(request, "utenti/templates/profile_page.html", context=context)


@login_required
def edit_profile(request, username):
    utente = Utente.objects.get(username=username)
    form = UserProfileEditForm(instance=utente.utente_base)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=request.user.utente_base)
        if form.is_valid():
            utente.first_name = form.cleaned_data['first_name']

            # Aggiornamento dell'immagine del profilo
            if form.cleaned_data['profile_picture'] != None:
                utente.utente_base.img = form.cleaned_data['profile_picture']

            # Aggiornamento dell'immagine della copertina
            if form.cleaned_data.get('cover_picture'):  # Controlla se c'è una nuova immagine di copertina
                utente.utente_base.cover_img = form.cleaned_data['cover_picture']

            utente.utente_base.save()
            utente.save()
            return redirect('profile_page', username=request.user.username)
    else:
        if request.user.username == username:
            return render(request, "utenti/templates/profile_edit.html", {"user": utente, "form": form})
        else:
            return redirect('pagina_non_autorizzata')

    return render(request, 'profile_edit.html', {'form': form})



@login_required
def edit_profile_organizer(request, username):
    utente = Utente.objects.get(username=username)
    form = OrganizzatoreProfileEditForm(instance=utente.utente_organizzatore)
    if request.method == 'POST':
        form = OrganizzatoreProfileEditForm(
            request.POST, request.FILES, instance=utente.utente_organizzatore)
        if form.is_valid():
            if form.cleaned_data['profile_picture'] != None:
                utente.utente_organizzatore.img = form.cleaned_data['profile_picture']
            
            # Aggiornamento dell'immagine della copertina
            if form.cleaned_data.get('cover_picture'):  # Controlla se c'è una nuova immagine di copertina
                utente.utente_organizzatore.cover_img = form.cleaned_data['cover_picture']

            utente.utente_organizzatore.save()
            utente.save()
            return redirect('profile_page', username=utente.username)
    else:
        if request.user.username == username:
            return render(request, "utenti/templates/profile_edit.html", {"user": utente, "form": form})
        else:
            return redirect('pagina_non_autorizzata')

    return render(request, 'profile_edit.html', {'form': form})

    

@login_required
def partecipa_evento(request, evento_id):
    if request.user.role != "organizzatore":
        evento = get_object_or_404(Evento, id=evento_id)
        if evento in request.user.utente_base.eventi_part.all():
            request.user.utente_base.eventi_part.remove(evento)
        else:
            request.user.utente_base.eventi_part.add(evento)
        return redirect('eventi:event_details', evento_id=evento_id)
    else:
        return redirect('pagina_non_autorizzata')
@login_required
def update_private_events(request):
    if request.method == 'POST':
        private_events = request.POST.get('private_events')  
        request.user.utente_base.private_future_events = private_events.capitalize()
        request.user.utente_base.save()  
        return JsonResponse({'status': 'success'})

def notifications(request):
    if request.user.is_authenticated:
        notifiche = Notifica.objects.filter(user=request.user).order_by('-data_creazione')
        return render(request, 'utenti/templates/notifications.html', {'notifiche': notifiche})
    else:
        return redirect('pagina_non_autorizzata')

@csrf_exempt
def accetta_richiesta_amicizia(request):
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        print(notification_id)
        try:
            notifica = Notifica.objects.get(pk=notification_id) # Ad esempio, se stai cercando per primary key
        except Notifica.DoesNotExist:
            # Qui puoi decidere come gestire l'errore, ad esempio:
            return "Notifica non trovata"

        # Aggiungi l'amicizia
        user = notifica.user
        mittente = notifica.mittente

        user.utente_base.amici.add(mittente.utente_base)

        # Segna la notifica come letta o eliminala
        notifica.delete()  # oppure: notifica.letta = True; notifica.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def get_unread_notifications_count(request):
    count = 0
    if request.user.is_authenticated:
        count = request.user.notifications.filter(letta=False).count()
    return JsonResponse({"unread_count": count})


@login_required
def send_friend_request(request, username):
    try:
        recipient = Utente.objects.get(username=username)
    except Utente.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Utente non trovato.'})

    # Verifica che l'utente non stia inviando una richiesta a se stesso.
    if request.user == recipient:
        return JsonResponse({'status': 'error', 'message': "Non puoi inviare una richiesta di amicizia a te stesso."})

    # Crea una notifica per l'utente selezionato
    notifica = Notifica(
        user=recipient,
        tipo=Notifica.RICHIESTA_AMICIZIA,
        testo=f"{request.user.username} ti ha inviato una richiesta di amicizia.",
        mittente=request.user
    )
    notifica.save()

    return JsonResponse({'status': 'success'})

def sono_amici(utente1, utente2):
    # Verifica se utente2 è nella lista degli amici di utente1
    return utente2 in utente1.amici.all()

def check_friend_request_status(request, destinatario_username):
    # Assicuriamoci che l'utente sia loggato
    if not request.user.is_authenticated:
        # Puoi gestire questo caso come preferisci. Potresti reindirizzare l'utente, mostrare un messaggio di errore, ecc.
        return render(request, "error_page.html", {"message": "Devi effettuare l'accesso per eseguire questa azione."})

    mittente = request.user
    destinatario = Utente.objects.get(username=destinatario_username)

    # Verifica se esiste una notifica di richiesta di amicizia
    notifica = Notifica.objects.filter(
        mittente=mittente,
        user=destinatario,
        tipo=Notifica.RICHIESTA_AMICIZIA
    ).first()

    # Se la notifica non esiste
    if not notifica:
        return 0
    # Se gli utenti sono amici
    elif sono_amici(mittente, destinatario):
        return 2
    # Se la notifica esiste ma gli utenti non sono ancora amici
    else:
        return 1
    
    
def tickets_page(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user)
        context = {
            'tickets': tickets
        }

        return render(request, 'utenti/templates/tickets.html', context)
    else:
        return redirect('pagina_non_autorizzata')