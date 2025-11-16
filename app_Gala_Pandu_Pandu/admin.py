from django.contrib import admin
from .models import Categoria,Usuario,Candidato,Voto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("icone", "titulo", "descricao", "criado_em")
    search_fields = ("titulo", "descricao")


admin.site.register(Usuario)

admin.site.register(Candidato)

admin.site.register(Voto)
