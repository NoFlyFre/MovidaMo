from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('', map, name='map'),
]