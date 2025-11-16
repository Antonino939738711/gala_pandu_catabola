from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
class CadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["nome", "sobrenome", "email", "foto", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = "votante"  # padrão
        if commit:
            user.save()
        return user
