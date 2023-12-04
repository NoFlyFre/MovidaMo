from django.urls import path
from . import views

app_name = 'eventi'

urlpatterns = [
    path('<int:evento_id>/', views.event_details, name='event_details'),
    path('', views.filter_events, name='filter_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('delete/<int:evento_id>/', views.delete_event, name='delete_event'),
    path('edit/<int:evento_id>/', views.edit_event, name='edit_event'),
]