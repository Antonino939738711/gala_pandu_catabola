from django.urls import path
from .views import login_view,cadastro_view,home,sair
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('',login_view,name='login'),
    path('cadastro',cadastro_view,name='cadastro'),
    path('home',home,name='home'),
    path('votacao/', views.pagina_votacao, name='pagina_votacao'),
    path('votar/<int:candidato_id>/', views.votar, name='votar'),
    path('sair/',sair,name='sair'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


