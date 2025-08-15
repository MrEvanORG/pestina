"""
WSGI config for pestina project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import threading

from django.core.wsgi import get_wsgi_application
from products.addons import cleanup_waited_phones

threading.Thread(target=cleanup_waited_phones,daemon=True).start()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestina.settings')
#wsgi.py

application = get_wsgi_application()