"""
WSGI config for volunteerhub project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volunteerhub.settings')

application = get_wsgi_application()
