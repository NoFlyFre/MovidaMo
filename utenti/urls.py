from django.urls import path
from movidamo.views import *
from utenti.views import *

urlpatterns = [
    path('signup/', register_request, name='signup'),
    path('signup_organizer/', register_request_organizer, name='signup_organizer'),   
    path('login/', login_request, name='login'),   
    path('logout/', logout_request, name='logout'),
    path('profile/<str:username>', profile_page, name='profile_page'),
    path('profile/<str:username>/edit', edit_profile, name='edit_profile'),
    path('profile/organizer/<str:username>/edit', edit_profile_organizer, name='edit_profile_organizer'),
    path('partecipa/<int:evento_id>/', partecipa_evento, name='partecipa_evento'),
    path('profile/update_private_events/', update_private_events, name='update_private_events'),
]