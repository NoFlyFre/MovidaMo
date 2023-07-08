from django.test import TestCase
from django.urls import reverse
from .models import Utente

class RegistrationTest(TestCase):
    def test_registration_success(self):
        # Crea un utente di prova
        username = 'testuser'
        password = 'testpassword'
        email = 'testuser@example.com'
        
        # Simula una richiesta POST per la registrazione
        response = self.client.post(reverse('signup'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
        })
        
        # Verifica che la registrazione abbia successo
        self.assertEqual(response.status_code, 302)  # Controllo il codice di stato della risposta (302: Redirection)
        self.assertRedirects(response, reverse('edit_profile', kwargs={'username': username}))  # Controllo il reindirizzamento alla pagina di modifica del profilo
        
        # Verifica che l'utente sia stato creato correttamente nel database
        self.assertTrue(Utente.objects.filter(username=username).exists())
        
        # Verifica che l'utente sia loggato dopo la registrazione
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_registration_failure_existing_user(self):
        # Crea un utente di prova già esistente nel database
        username = 'existinguser'
        password = 'existingpassword'
        email = 'existinguser@example.com'
        Utente.objects.create_user(username=username, password=password, email=email)
        
        # Simula una richiesta POST per la registrazione con le stesse credenziali
        response = self.client.post(reverse('signup'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
        })
        
        # Verifica che la registrazione fallisca a causa delle credenziali già esistenti
        self.assertEqual(response.status_code, 200)  # Controllo il codice di stato della risposta (200: OK)
        self.assertContains(response, 'Un utente con questo nome')  # Controllo il messaggio di errore restituito
        
        # Verifica che l'utente non sia stato creato nuovamente nel database
        self.assertFalse(len(Utente.objects.filter(username=username))>1)
        
    def test_registration_failure_bad_email(self):
        # Crea un utente di prova già esistente nel database
        username = 'testuser'
        password = 'testpassword'
        email = 'testuser_not_an_email'
                
        # Simula una richiesta POST per la registrazione con le stesse credenziali
        response = self.client.post(reverse('signup'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
        })
        
        # Verifica che la registrazione fallisca a causa della mail non corretta
        self.assertEqual(response.status_code, 200)  # Controllo il codice di stato della risposta (200: OK)
        self.assertContains(response, 'Inserisci un indirizzo email valido')  # Controllo il messaggio di errore restituito
        
        # Verifica che l'utente non sia stato creato
        self.assertFalse(len(Utente.objects.filter(username=username))==1)
        
    def test_registration_failure_common_password(self):
        # Crea un utente di prova già esistente nel database
        username = 'testuser'
        password = 'prova'
        email = 'testuser@example.com'
                
        # Simula una richiesta POST per la registrazione con le stesse credenziali
        response = self.client.post(reverse('signup'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
        })
                
        # Verifica che la registrazione fallisca a causa della password troppo comune
        self.assertEqual(response.status_code, 200)  # Controllo il codice di stato della risposta (200: OK)
                
        self.assertContains(response, 'Questa password è troppo comune.')  # Controllo il messaggio di errore restituito
        
        # Verifica che l'utente non sia stato creato
        self.assertFalse(len(Utente.objects.filter(username=username))==1)
        
    def test_registration_failure_short_password(self):
        # Crea un utente di prova già esistente nel database
        username = 'testuser'
        password = 'prv'
        email = 'testuser@example.com'
                
        # Simula una richiesta POST per la registrazione con le stesse credenziali
        response = self.client.post(reverse('signup'), {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
        })
        
        # Verifica che la registrazione fallisca a causa della password troppo corta
        self.assertEqual(response.status_code, 200)  # Controllo il codice di stato della risposta (200: OK)        
        self.assertContains(response, 'Questa password è troppo corta.')  # Controllo il messaggio di errore restituito
        
        # Verifica che l'utente non sia stato creato
        self.assertFalse(len(Utente.objects.filter(username=username))==1)

        