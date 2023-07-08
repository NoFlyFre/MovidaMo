from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.db import transaction
from .models import Organizzatore, Utente, UtenteBase
from django import forms


class UtenteSignUpForm(UserCreationForm):
        
    class Meta(UserCreationForm.Meta):
        model = Utente
        fields = ['username', 'email', 'password1', 'password2']
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            print("salvataggio")
            user.save()
        utente = UtenteBase.objects.create(utente=user)
        utente.img = "../static/default_profile.png"
        utente.save()
        return user

class UtenteLoginForm(AuthenticationForm):
    class Meta:
        model = Utente
        fields = ['username', 'password']
        
class UserProfileEditForm(UserChangeForm):
    first_name = forms.CharField(label='Nome', max_length=100)
    profile_picture = forms.ImageField(label='Immagine del profilo', required=False)

    class Meta:
        model = UtenteBase
        fields = ('first_name', 'profile_picture')
    
class OrganizzatoreSignUpForm(UserCreationForm):
    
    name = forms.CharField(label='Nome', max_length=100)
    
    class Meta(UserCreationForm.Meta):
        model = Utente
        fields = ['username','name', 'email', 'password1', 'password2']
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.role = Utente.Role.ORGANIZZATORE
        if commit:
            print("salvataggio")
            
            user.save()
        utente = Organizzatore.objects.create(utente=user)
        utente.img = "../static/default_profile.png"
        utente.nome = self.cleaned_data.get('name')
        utente.save()
        return user
    
class OrganizzatoreProfileEditForm(UserChangeForm):
    profile_picture = forms.ImageField(label='Immagine del profilo', required=False)

    class Meta:
        model = Organizzatore
        fields = ('profile_picture',)
    

    


