from django.db import models
import datetime

from utenti.models import Organizzatore

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorie"

class Evento(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    cap = models.CharField(max_length=5)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE)
    data = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    special_guest = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # Campo per memorizzare le parole chiave separate da virgola
    tags = models.CharField(max_length=200, null=True, blank=True)
    mappa_lat = models.FloatField(blank=True, null=True)
    mappa_long = models.FloatField(blank=True, null=True)
    image = models.ImageField(
        upload_to='eventi/immagini', null=True, blank=True)
    tickets_link = models.URLField(null=True, blank=True)
    info_phone_number = models.CharField(max_length=20, null=True, blank=True)
    

    class Meta:
        verbose_name_plural = "Eventi"

    def __str__(self):
        out = str(self.data.strftime("%d/%m/%Y")) + " - " + self.name + " at " + self.location + " on " + \
            " (" + self.categoria.nome + ")"
        return out

    def is_free(self):
        return self.price == 0

    def get_image_url(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        else:
            return ''

    def format_price(self):
        float_price = float(self.price)
        if float_price.is_integer():
            return '{:,.0f} €'.format(float_price)
        else:
            return '{:,.2f} €'.format(float_price)

    def data_evento_formattata(self):
        return self.data.strftime("%A, %d/%m/%y").title()

    def data_evento_formattata_long(self):
        return self.data.strftime("%A, %d %B %Y").title()

    def is_today(self):
        return self.data == datetime.date.today()

    def formatted_tags(self):
        if not self.tags:
            return ''
        formatted_tags = ", ".join([tag.strip().capitalize()
                                   for tag in self.tags.split(",")])
        return formatted_tags

    def formatted_time(self):
        return self.time.strftime("%H:%M")

    def has_special_guest(self):
        return bool(self.special_guest)
    
    def formatted_coord(self):
        return f"{self.mappa_lat:.6f}, {self.mappa_long:.6f}"
    
    def get_organizzatore(self):
        organizer = Organizzatore.objects.filter(eventi=self).first()
        return organizer
    
    def is_past(self):
        return self.data < datetime.date.today()
    
    def get_day(self):
        return self.data.strftime("%d")
    
    def get_month(self):
        return self.data.strftime("%B").capitalize()[:3]