
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projecto_Gala_Pandu_Pandu.settings')

application = get_asgi_application()
