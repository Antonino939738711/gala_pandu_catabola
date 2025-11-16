import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projecto_Gala_Pandu_Pandu.settings')

app = get_wsgi_application()  # precisa ser "app", não "application"
