import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from utenti.models import Utente, Organizzatore
from eventi.models import Evento, Categoria
from django.contrib import auth


class EventCreationTest(TestCase):
    def setUp(self):
        self.user = Utente.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        # Assegna il valore corretto al campo role
        self.user.role = Utente.Role.ORGANIZZATORE
        self.user.save()

        self.user_profile = Organizzatore.objects.create(
            utente=self.user,
            img='default_profile.png',
        )
    
        self.categoria = Categoria.objects.create(nome='Aperitivo')

    def test_event_creation(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })

        # Verifica reindirizzamento
        self.assertEqual(response.status_code, 302)
        
        # Verifica che l'evento sia stato creato
        self.assertTrue(Evento.objects.exists())

    def test_event_creation_no_login(self):

        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })

        # Verifica reindirizzamento
        self.assertEqual(response.status_code, 302)

        # Verifica che l'evento sia stato creato
        self.assertFalse(Evento.objects.exists())

    def test_event_creation_base_user(self):

        # Assegna il valore corretto al campo role
        self.user.role = Utente.Role.UTENTE_BASE
        self.user.save()

        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })

        # Verifica reindirizzamento
        self.assertEqual(response.status_code, 302)
        # Verifica che l'evento sia stato creato
        self.assertFalse(Evento.objects.exists())

    def test_event_creation_missing_info(self):

        response = self.client.post(reverse('eventi:add_event'), {
            'name': '',
            'location': 'Venue',
            'address': '',
            'cap': '',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })

        # Verifica reindirizzamento
        self.assertEqual(response.status_code, 302)

        # Verifica che l'evento sia stato creato
        self.assertFalse(Evento.objects.exists())

class EventEditTest(TestCase):
    
    def setUp(self):
        self.user = Utente.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        # Assegna il valore corretto al campo role
        self.user.role = Utente.Role.ORGANIZZATORE
        self.user.save()
        
        self.user_profile = Organizzatore.objects.create(
            utente=self.user,
            img='default_profile.png',
        )
        
        self.user2 = Utente.objects.create_user(
            username='testuser2',
            password='testpassword2',
        )
        # Assegna il valore corretto al campo role
        self.user2.role = Utente.Role.ORGANIZZATORE
        self.user2.save()

        self.user_profile2 = Organizzatore.objects.create(
            utente=self.user2,
            img='default_profile.png',
        )

        self.categoria = Categoria.objects.create(nome='Aperitivo')

    def test_event_edit(self):
        
        # Effettua il login come utente
        self.client.login(username='testuser', password='testpassword')
                
        # Crea l'evento da modificare nel database
        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })
        
        evento = self.user_profile.eventi.first()
        
        # Esegui la richiesta POST per modificare l'evento
        response = self.client.post(reverse('eventi:edit_event', args=[evento.pk]), {
            'name': 'Nuovo nome',
            'location': 'Nuova location',
            'address': 'Nuovo indirizzo',
            'cap': '54321',
            'categoria': self.categoria.id,
            'data': '2023-07-06',
            'time': '20:00',
            'price': '30.00',
            'special_guest': 'Jane Doe',
            'description': 'Concerto aggiornato',
            'tags': 'musica, aggiornamento',
            'tickets_link': 'https://example.com/updated',
            'info_phone_number': '987-654-3210',
        })

        
        # Verifica che la modifica sia stata effettuata correttamente
        self.assertEqual(response.status_code, 302)  # Verifica reindirizzamento

        # Verifica che l'evento sia stato modificato nel database
        evento.refresh_from_db()
        self.assertEqual(evento.name, 'Nuovo nome')
        self.assertEqual(evento.location, 'Nuova location')
        self.assertEqual(evento.address, 'Nuovo indirizzo')
        self.assertEqual(evento.cap, '54321')
        self.assertEqual(evento.data, datetime.date(2023, 7, 6))
        self.assertEqual(evento.time, datetime.time(20, 0))
        self.assertEqual(evento.price, Decimal('30.00'))
        self.assertEqual(evento.special_guest, 'Jane Doe')
        self.assertEqual(evento.description, 'Concerto aggiornato')
        self.assertEqual(evento.tags, 'musica, aggiornamento')
        self.assertEqual(evento.tickets_link, 'https://example.com/updated')
        self.assertEqual(evento.info_phone_number, '987-654-3210')
        
    def test_event_edit_no_login(self):
        
        # Crea l'evento da modificare nel database
        evento = Evento.objects.create(
            name='Concerto',
            location='Venue',
            address='123 Main St',
            cap='12345',
            categoria=self.categoria,
            data='2023-07-05',
            time='19:00',
            price='20.00',
            special_guest='John Doe',
            description='Concerto di musica',
            tags='musica, concerto',
            tickets_link='https://example.com',
            info_phone_number='123-456-7890',
        )
        
        # Esegui la richiesta POST per modificare l'evento
        response = self.client.post(reverse('eventi:edit_event', args=[evento.pk]), {
            'name': 'Nuovo nome',
            'location': 'Nuova location',
            'address': 'Nuovo indirizzo',
            'cap': '54321',
            'categoria': self.categoria.id,
            'data': '2023-07-06',
            'time': '20:00',
            'price': '30.00',
            'special_guest': 'Jane Doe',
            'description': 'Concerto aggiornato',
            'tags': 'musica, aggiornamento',
            'tickets_link': 'https://example.com/updated',
            'info_phone_number': '987-654-3210',
        })
        
        # Verifica che la modifica sia stata effettuata correttamente
        self.assertEqual(response.status_code, 302)  # Verifica reindirizzamento

        # Verifica che l'evento sia stato modificato nel database
        evento.refresh_from_db()
        self.assertNotEqual(evento.name, 'Nuovo nome')
        self.assertNotEqual(evento.location, 'Nuova location')
        self.assertNotEqual(evento.address, 'Nuovo indirizzo')
        self.assertNotEqual(evento.cap, '54321')
        self.assertNotEqual(evento.data, datetime.date(2023, 7, 6))
        self.assertNotEqual(evento.time, datetime.time(20, 0))
        self.assertNotEqual(evento.price, Decimal('30.00'))
        self.assertNotEqual(evento.special_guest, 'Jane Doe')
        self.assertNotEqual(evento.description, 'Concerto aggiornato')
        self.assertNotEqual(evento.tags, 'musica, aggiornamento')
        self.assertNotEqual(evento.tickets_link, 'https://example.com/updated')
        self.assertNotEqual(evento.info_phone_number, '987-654-3210')
        
    def test_event_edit_no_event_organizer(self):
                        
        # Effettua il login come utente 1
        self.client.login(username='testuser', password='testpassword')
                
        # Crea l'evento da modificare nel database
        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })
        
        evento = self.user_profile.eventi.first()
        
        # Effettua il logout come user 1
        self.client.logout()
        
        # Effettua il login come utente 2
        self.client.login(username='testuser2', password='testpassword2')
        
        # Esegui la richiesta POST per modificare l'evento
        response = self.client.post(reverse('eventi:edit_event', args=[evento.pk]), {
            'name': 'Nuovo nome',
            'location': 'Nuova location',
            'address': 'Nuovo indirizzo',
            'cap': '54321',
            'categoria': self.categoria.id,
            'data': '2023-07-06',
            'time': '20:00',
            'price': '30.00',
            'special_guest': 'Jane Doe',
            'description': 'Concerto aggiornato',
            'tags': 'musica, aggiornamento',
            'tickets_link': 'https://example.com/updated',
            'info_phone_number': '987-654-3210',
        })
        
        # Verifica che la modifica sia stata effettuata correttamente
        self.assertEqual(response.status_code, 302)  # Verifica reindirizzamento

        # Verifica che l'evento sia stato modificato nel database
        evento.refresh_from_db()
        self.assertNotEqual(evento.name, 'Nuovo nome')
        self.assertNotEqual(evento.location, 'Nuova location')
        self.assertNotEqual(evento.address, 'Nuovo indirizzo')
        self.assertNotEqual(evento.cap, '54321')
        self.assertNotEqual(evento.data, datetime.date(2023, 7, 6))
        self.assertNotEqual(evento.time, datetime.time(20, 0))
        self.assertNotEqual(evento.price, Decimal('30.00'))
        self.assertNotEqual(evento.special_guest, 'Jane Doe')
        self.assertNotEqual(evento.description, 'Concerto aggiornato')
        self.assertNotEqual(evento.tags, 'musica, aggiornamento')
        self.assertNotEqual(evento.tickets_link, 'https://example.com/updated')
        self.assertNotEqual(evento.info_phone_number, '987-654-3210')
                
        # Effettua il login come utente
        self.client.login(username='testuser', password='testpassword')
                
        # Crea l'evento da modificare nel database
        response = self.client.post(reverse('eventi:add_event'), {
            'name': 'Concerto',
            'location': 'Venue',
            'address': '123 Main St',
            'cap': '12345',
            'categoria': self.categoria.id,
            'data': '2023-07-05',
            'time': '19:00',
            'price': '20.00',
            'special_guest': 'John Doe',
            'description': 'Concerto di musica',
            'tags': 'musica, concerto',
            'tickets_link': 'https://example.com',
            'info_phone_number': '123-456-7890',
        })
        
        evento = self.user_profile.eventi.first()
        
        # Esegui la richiesta POST per modificare l'evento
        response = self.client.post(reverse('eventi:edit_event', args=[evento.pk]), {
            'name': '',
            'location': 'Nuova location',
            'address': '',
            'cap': '',
            'categoria': self.categoria.id,
            'data': '2023-07-06',
            'time': '',
            'price': '30.00',
            'special_guest': 'Jane Doe',
            'description': 'Concerto aggiornato',
            'tags': 'musica, aggiornamento',
            'tickets_link': 'https://example.com/updated',
            'info_phone_number': '987-654-3210',
        })

        
        # Verifica che la modifica sia stata effettuata correttamente
        self.assertEqual(response.status_code, 302)  # Verifica reindirizzamento

        # Verifica che l'evento sia stato modificato nel database
        evento.refresh_from_db()
        self.assertNotEqual(evento.name, 'Nuovo nome')
        self.assertNotEqual(evento.location, 'Nuova location')
        self.assertNotEqual(evento.address, 'Nuovo indirizzo')
        self.assertNotEqual(evento.cap, '54321')
        self.assertNotEqual(evento.data, datetime.date(2023, 7, 6))
        self.assertNotEqual(evento.time, datetime.time(20, 0))
        self.assertNotEqual(evento.price, Decimal('30.00'))
        self.assertNotEqual(evento.special_guest, 'Jane Doe')
        self.assertNotEqual(evento.description, 'Concerto aggiornato')
        self.assertNotEqual(evento.tags, 'musica, aggiornamento')
        self.assertNotEqual(evento.tickets_link, 'https://example.com/updated')
        self.assertNotEqual(evento.info_phone_number, '987-654-3210')
