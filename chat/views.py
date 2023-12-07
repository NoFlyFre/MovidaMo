from django.shortcuts import render
from chat.models import ChatRoom, Message
from django.db.models import Q
import datetime
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utenti.models import Utente
from django.db.models import Max

def chat_list(request):
    # Ottieni l'ID dell'ultimo messaggio per ogni chat room
    last_messages = Message.objects.filter(
        room__in=ChatRoom.objects.filter(
            Q(participante1=request.user) | Q(participante2=request.user)
        )
    ).values('room').annotate(last_msg_id=Max('id'))

    # Crea un dizionario per mappare l'ID della chat room all'ID dell'ultimo messaggio
    room_to_last_msg = {lm['room']: lm['last_msg_id'] for lm in last_messages}

    chat_details = []

    # Ottieni le chat room ordinate in base all'ID dell'ultimo messaggio
    for room_id, last_msg_id in sorted(room_to_last_msg.items(), key=lambda x: x[1], reverse=True):
        room = ChatRoom.objects.get(id=room_id)
        other_user = room.participante1 if room.participante2 == request.user else room.participante2

        last_message = Message.objects.get(id=last_msg_id)
        time_diff = humanize_time_diff(last_message.timestamp)

        chat_details.append({
            'room_id': room.id,
            'other_name': other_user.utente_organizzatore.nome,
            'other_user_image': other_user.utente_organizzatore.img.url if other_user.utente_organizzatore.img else None,
            'last_message': last_message.message,
            'time_diff': time_diff,
        })

    return render(request, 'chat/templates/chat_list.html', {'chat_details': chat_details})



def chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    messages = Message.objects.filter(room=chat_room).order_by('timestamp')
    
    # Determina l'altro partecipante
    if request.user == chat_room.participante1:
        other_user = chat_room.participante2
    else:
        other_user = chat_room.participante1

    # Ottieni il nome e l'immagine dell'altro partecipante
    if hasattr(other_user, 'utente_organizzatore'):
        other_profile_img_url = other_user.utente_organizzatore.img.url
        other_profile_name = other_user.utente_organizzatore.nome
    elif hasattr(other_user, 'utente_base'):
        other_profile_img_url = other_user.utente_base.img.url
        other_profile_name = other_user.utente_base.nome
    else:
        other_profile_img_url = None  # o un URL di immagine di default
        other_profile_name = other_user.username  # nome di default

    messages_with_profile = []
    for message in messages:
        sender = message.sender
        if hasattr(sender, 'utente_organizzatore'):
            profile_img_url = sender.utente_organizzatore.img.url
        elif hasattr(sender, 'utente_base'):
            profile_img_url = sender.utente_base.img.url
        else:
            profile_img_url = None  # o un URL di immagine di default

        messages_with_profile.append({
            'text': message.message,
            'sender_username': sender.username,
            'profile_img_url': profile_img_url
        })
        
    print({
    'chat_room': chat_room,
    'messages_with_profile': messages_with_profile,
    'other_profile_img_url': other_profile_img_url,
    'other_profile_name': other_profile_name,
    })

    return render(request, 'chat/templates/chat_room.html', {
        'chat_room': chat_room,
        'messages_with_profile': messages_with_profile,
        'other_profile_img_url': other_profile_img_url,
        'other_profile_name': other_profile_name,
    })



def humanize_time_diff(timestamp):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - timestamp

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = seconds // 3600
    days = seconds // 86400

    if days > 0:
        return f" ∙ {int(days)}d"
    elif hours > 0:
        return f" ∙ {int(hours)}h"
    elif minutes > 0:
        return f" ∙ {int(minutes)}m"
    else:
        return f" ∙ {int(seconds)}s"


@login_required
def start_chat(request, user_id):
    # Assumi che 'user_id' sia l'ID dell'utente con cui si vuole iniziare la chat
    user1 = request.user
    user2 = Utente.objects.get(id=user_id)  # Sostituisci con la logica appropriata per ottenere user2

    chat_room = get_or_create_chat_room(user1, user2)

    # Reindirizza all'URL della chat room
    return redirect('chat:chat_room', room_id=chat_room.id)


def get_or_create_chat_room(user1, user2):
    chat_room = ChatRoom.objects.filter(
        Q(participante1=user1, participante2=user2) | Q(participante1=user2, participante2=user1)
    ).first()

    if not chat_room:
        chat_room = ChatRoom.objects.create(participante1=user1, participante2=user2)

    return chat_room