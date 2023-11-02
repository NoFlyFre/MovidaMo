"""
WSGI config for movidamo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
'''
import locale

locale.setlocale(locale.LC_TIME, 'it_IT.utf8')
'''

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movidamo.settings')

application = get_wsgi_application()
