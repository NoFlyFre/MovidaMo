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
    path('notifications/', notifications, name='notifications'),
    path('notifications/accept_friend_request', accetta_richiesta_amicizia, name='accetta_richiesta_amicizia'),
    path('check_notifications/', check_notifications, name='check_notifications'),
    path('unread_count/', get_unread_notifications_count, name="unread_notifications_count"),
    path('mark_notifications_as_read/', mark_notifications_ad_read, name="mark_notifications_as_read"),
    path('send_friend_request/<str:username>/', send_friend_request, name='send_friend_request'),
    path('tickets/', tickets_page, name='tickets_page'),
]