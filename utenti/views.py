from django.shortcuts import render
from django.utils import timezone
from utenti.forms import OrganizzatoreProfileEditForm, OrganizzatoreSignUpForm, UserProfileEditForm, UtenteSignUpForm, UtenteLoginForm
from utenti.models import Utente
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from movidamo.views import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



def register_request(request):
    if request.method == "POST":
        form = UtenteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(edit_profile_organizer, username=request.user.username)
        
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
    # Eventi passati
    if utente.role == "organizzatore":
        tot_events = utente.utente_organizzatore.eventi.count()
        eventi_passati = utente.utente_organizzatore.eventi.filter(
            data__lt=timezone.now()).order_by('-data')
        # Eventi futuri
        eventi_futuri = utente.utente_organizzatore.eventi.filter(
            data__gte=timezone.now()).order_by('data')
    else:
        tot_events = utente.utente_base.eventi_part.count()
        eventi_passati = utente.utente_base.eventi_part.filter(
            data__lt=timezone.now()).order_by('-data')
        # Eventi futuri
        eventi_futuri = utente.utente_base.eventi_part.filter(
            data__gte=timezone.now()).order_by('data')  

    context = {'profile_user': utente,
               'eventi_pass': eventi_passati, 'eventi_fut': eventi_futuri,
               'tot_events': tot_events}

    return render(request, "utenti/templates/profile_page.html", context=context)


@login_required
def edit_profile(request, username):
    utente = Utente.objects.get(username=username)
    form = UserProfileEditForm(instance=utente.utente_base)
    if request.method == 'POST':
        form = UserProfileEditForm(
            request.POST, request.FILES, instance=request.user.utente_base)
        if form.is_valid():
            utente.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['profile_picture'] != None:
                utente.utente_base.img = form.cleaned_data['profile_picture']
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
    utente.role = "organizzatore"
    form = OrganizzatoreProfileEditForm(instance=utente.utente_organizzatore)
    if request.method == 'POST':
        form = OrganizzatoreProfileEditForm(
            request.POST, request.FILES, instance=request.user.utente_organizzatore)
        if form.is_valid():
            if form.cleaned_data['profile_picture'] != None:
                utente.utente_organizzatore.img = form.cleaned_data['profile_picture']
                utente.utente_organizzatore.save()
            utente.save()
            return redirect('profile_page', username=request.user.username)
    else:
        if request.user.username == username:
            return render(request, "utenti/templates/profile_edit.html", {"user": utente, "form": form})
        else:
            return redirect('pagina_non_autorizzata')

    

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


