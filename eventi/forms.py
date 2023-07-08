from django import forms
from .models import Evento, Categoria


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'name',
            'location',
            'address',
            'cap',
            'categoria',
            'data',
            'time',
            'price',
            'special_guest',
            'description',
            'tags',
            'mappa_lat',
            'mappa_long',
            'image',
            'tickets_link',
            'info_phone_number',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'cap': forms.NumberInput(attrs={'type': 'number', 'pattern': '[0-9]{5}'}),
        }

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'name',
            'location',
            'address',
            'cap',
            'categoria',
            'data',
            'time',
            'price',
            'special_guest',
            'description',
            'tags',
            'mappa_lat',
            'mappa_long',
            'image',
            'tickets_link',
            'info_phone_number',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'cap': forms.NumberInput(attrs={'type': 'number', 'pattern': '[0-9]{5}'}),
        }
