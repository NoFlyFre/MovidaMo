import json
from django.shortcuts import get_object_or_404, render
import jwt
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from eventi.models import Evento
from utenti.models import Utente
from django.views.decorators.http import require_POST
from .models import Ticket, Transaction
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Inizializza il client di Stripe con la tua chiave segreta
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
stripe.api_version = "2023-10-16"
token_secret_key = settings.TOKEN_SECRET_KEY.encode()

def create_stripe_account(request):
    user_profile = request.user
    # Assicurati che l'utente sia autenticato e sia un organizzatore
    if request.user.is_authenticated and request.user.role == Utente.Role.ORGANIZZATORE:
        # Crea un nuovo account Stripe Connect
        account = stripe.Account.create(
            type="express",
            capabilities={
                'card_payments': {'requested': True},
                'transfers': {'requested': True},
            },
        )
        
        # Memorizza l'ID dell'account Stripe nell'oggetto Organizzatore
        request.user.utente_organizzatore.stripe_account_id = account.id
        request.user.utente_organizzatore.save()
        
        # Inizia il processo di onboarding
        return start_stripe_onboarding(request, account.id, user_profile)
    else:
        # Gestisci l'errore o reindirizza l'utente altrove
        pass

def start_stripe_onboarding(request, account_id, user):
    # Crea un link di onboarding per l'account creato
    account_link = stripe.AccountLink.create(
        account=account_id,
        refresh_url=request.build_absolute_uri(f'/profile/{user.username}/edit'),
        return_url=request.build_absolute_uri('/'),
        type='account_onboarding',
    )
    # Reindirizza l'utente al link di onboarding
    return account_link.url

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        
        user_id, event_id, organizer_stripe_account_id, price_id = decode_token(token)
                
        try:
            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price":price_id, "quantity": 1}],
                payment_intent_data={
                    "application_fee_amount": 200,
                },
                success_url = f"http://127.0.0.1:8000/payment/success_order/?token={token}",
                cancel_url="http://127.0.0.1:8000/",
                stripe_account=organizer_stripe_account_id,
                metadata={
                    'token': token,
                },
            )
                        
            return JsonResponse({'url': checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())

def send_ticket_email(user, event, ticket, subject, template_name, from_email, to_email):
    html_message = render_to_string(template_name, {'user': user, 'event': event, 'ticket': ticket})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    try:
        event = stripe.Webhook.construct_event(
            request.body, 
            request.META.get('HTTP_STRIPE_SIGNATURE'), 
            settings.STRIPE_LINKED_ACCOUNTS_WEBHOOK_KEY
        )
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        token = session['metadata'].get('token')
        user_id, event_id, _, _ = decode_token(token)

        try:
            user = Utente.objects.get(pk=user_id)
            event = Evento.objects.get(pk=event_id)
        except (Utente.DoesNotExist, Evento.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'User or event not found'}, status=404)

        ticket = Ticket.objects.create(user=user, event=event)
        qr_data = {
            "ticket_id": str(ticket.pk),
            "user_id": str(user_id),
            "event_id": str(event_id),
            "event_name": event.name,
            "event_date": event.data.strftime("%Y-%m-%d"),
        }
        filebuffer = create_qr_code(qr_data)
        filename = f'tickets_qr/qr_code_{ticket.id}.png'
        ticket.qr_code.save(filename, filebuffer)
        ticket.save()

        Transaction.objects.create(
            user=user,
            ticket=ticket,
            amount=session.amount_total/100,
            transaction_id=session.id
        )

        send_ticket_email(
            user, event, ticket,
            "Dettagli del tuo biglietto per l'evento",
            'payment/templates/email_confirm.html',
            settings.DEFAULT_FROM_EMAIL,
            "fracali99@gmail.com"
        )

    return JsonResponse({'status': 'success'})

def decode_token(token):
    token_encoded = token.encode()
    decoded = jwt.decode(token_encoded, token_secret_key, algorithms=['HS256'])
    user_id = decoded['user_id']
    event_id = decoded['event_id']
    organizer_id = decoded['organizer_id']
    price_id = decoded['price_id']
    
    return user_id, event_id, organizer_id, price_id


def success_order(request):   
    token = request.GET.get('token') 
    user_id, event_id, organizer_stripe_account_id, price_id = decode_token(token)

    if request.user.is_authenticated and request.user.id == user_id:
        evento = Evento.objects.get(id=event_id)
        organizer = evento.get_organizzatore()
        
        
        ticket = Ticket.objects.filter(user_id=user_id, event_id=event_id).latest('created_at')
        
        context = {
            'name': evento.name,
            'data': evento.data,
            'prezzo': evento.price,
            'time': evento.time,
            'organizzatore': organizer.nome,
            'icon_img': organizer.img.url,
            'event_img': evento.image.url,
            'qr_code': ticket.qr_code.url if ticket.qr_code else None,
        }
        
        return render(request, 'utenti/templates/tickets_order.html', context)
    else:
        return redirect('/')

