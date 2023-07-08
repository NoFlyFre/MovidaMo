from django.contrib import admin
from django.urls import path, re_path, include
from movidamo.views import *
from django.conf import settings
from django.conf.urls.static import static
from utenti.views import *

urlpatterns = [
    #path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', home, name='homepage'),
    path('eventi/', include('eventi.urls')),
    path('user/', include('utenti.urls')),
    path('map/', include('mappa.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)