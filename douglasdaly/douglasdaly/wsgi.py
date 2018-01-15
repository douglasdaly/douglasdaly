"""
WSGI config for douglasdaly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import dotenv

dotenv.load_dotenv(os.path.abspath(os.path.join(os.pardir, os.pardir, '.env')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "douglasdaly.settings")

application = get_wsgi_application()
