from django.urls import path
from . import views

urlpatterns = [
    #path('stripe/refresh', views.stripe_refresh, name='stripe_refresh'),
    #path('stripe/return', views.stripe_return, name='stripe_return'),
    path('stripe/checkout_session', views.create_checkout_session, name='create_checkout_session'),
    path('stripe/webhook', views.stripe_webhook, name='stripe_webhook'),
    path('success_order/', views.success_order, name='success_order'),
]