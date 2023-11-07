from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Utente, UtenteBase
from django.core.files.base import ContentFile
import requests

class CustomUserSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        print(data)
        user = sociallogin.user
        provider = sociallogin.account.provider 

        # Logica per Google
        if provider == 'google':
            email = data.get('email')
            user.email = email
            username = email.split('@')[0]
            user.username = username

        # Logica per Facebook
        elif provider == 'facebook':
            email = data.get('email')
            user.email = email
            username = data.get('name').replace(' ', '').lower()
            user.username = username

        # Impostare nome e cognome che sono comuni sia a Google che a Facebook
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')

        # Impostazioni specifiche per il modello personalizzato di Utente
        user.role = Utente.Role.UTENTE_BASE  # o qualsiasi altro valore predefinito che desideri

        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not UtenteBase.objects.filter(utente=user).exists():
            # UtenteBase non esiste, quindi crealo
            extra_data = sociallogin.account.extra_data
            print(extra_data)
            provider = sociallogin.account.provider  # Anche qui, verifica il provider
            print(provider)

            # Imposta il nome da visualizzare
            nome = f"{user.first_name} {user.last_name}".strip()
            print(nome)

            # Gestisci la data di nascita e l'immagine del profilo in base al provider
            if provider == 'google':
                print('google')
                dob = extra_data.get('birthdate', None) 
                picture_url = extra_data.get('picture', None)

            elif provider == 'facebook':
                print('facebook')
                # Per Facebook, puoi accedere alla foto del profilo come mostrato di seguito
                picture_data = extra_data.get('picture', {}).get('data', {})
                picture_url = picture_data.get('url', None)
                # Facebook non fornisce la data di nascita per impostazione predefinita, potresti dover richiederla con permessi specifici

            utente_base = UtenteBase(utente=user, nome=nome)

            # Gestione dell'immagine del profilo
            if picture_url:
                response = requests.get(picture_url)
                print(response)
                if response.status_code == 200:
                    print(200)
                    utente_base.img.save(f"{user.username}_profile.jpg", ContentFile(response.content), save=False)
            utente_base.save()

        return user
