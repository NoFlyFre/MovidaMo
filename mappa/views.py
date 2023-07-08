from django.shortcuts import render
from eventi.models import *
from django.core.serializers import serialize


def map(request):
    eventi = Evento.objects.filter(
        data=datetime.date.today())
    categorie = Categoria.objects.all()
    serialized_eventi = serialize(
        'json', eventi, fields=('name', 'mappa_lat', 'mappa_long'))

    context = {
        'eventi_json': serialized_eventi,
        'eventi': eventi,
        'categorie': categorie
    }
    return render(request, '../templates/mappa/templates/map.html', context=context)
