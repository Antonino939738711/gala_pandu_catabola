from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages
from .models import Categoria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categoria, Candidato, Voto
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Count
from .models import Categoria, Candidato, Voto
from django.contrib.auth.decorators import user_passes_test



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")  
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            return render(request, "usuarios/login.html", {"error": "Email ou senha inválidos !"})
    return render(request, "usuarios/login.html")


def cadastro_view(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha1 = request.POST.get("password1")
        senha2 = request.POST.get("password2")
        foto = request.FILES.get("foto")

        if senha1 != senha2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "usuarios/cadastro.html")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Esse email já está cadastrado.")
            return render(request, "usuarios/cadastro.html")

        user = Usuario.objects.create_user(
            email=email,
            password=senha1,
            nome=nome,
            sobrenome=sobrenome,
            foto=foto
        )
        login(request, user)
        messages.success(request, "Cadastro realizado com sucesso!")
    return render(request, "usuarios/cadastro.html")

def home(request):
    categorias = Categoria.objects.all()
    return render(request, "usuarios/home.html", {"categorias": categorias})
@login_required
def pagina_votacao(request):
    categorias = Categoria.objects.prefetch_related("candidatos__usuario")

    contexto = []
    percent = 20
    for categoria in categorias:
        candidatos = list(categoria.candidatos.all())

        total_votos = sum([c.votos_totais for c in candidatos]) or 1  
        candidatos_ordenados = sorted(
            candidatos,
            key=lambda c: c.votos_totais,
            reverse=True
        )
        
        # 🎯 CORREÇÃO AQUI: Inicializamos a variável com 0.
        # Isso garante que 'percentagem' sempre terá um valor, mesmo que a categoria
        # não tenha candidatos e o loop 'for c in candidatos_ordenados' não seja executado.
        percentagem = 0 
        
        # adiciona percentual dentro dos objetos
        for c in candidatos_ordenados:
            c.percentual = int(round((c.votos_totais / total_votos) * 100, 2))
            percentagem = int(c.percentual) # A variável será sobrescrita aqui se houver candidatos

        contexto.append({
            "id": categoria.id,
            "icone": categoria.icone,
            "titulo": categoria.titulo,
            "descricao": categoria.descricao,
            "candidatos_ordenados": candidatos_ordenados,  
            "percentagem": percentagem, # Variável agora garantida
        })

    return render(request, "usuarios/votar.html", {"categorias": contexto,"percent":percent})


@login_required
def votar(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)
    categoria = candidato.categoria
    usuario = request.user
    if not usuario.pode_votar:
        messages.error(request, "Apenas votantes podem votar.")
        return redirect("pagina_votacao")

    if Voto.objects.filter(votante=usuario, categoria=categoria).exists():
        messages.error(request, f"Você já votou na categoria {categoria.titulo}.")
    else:
        Voto.objects.create(votante=usuario, candidato=candidato, categoria=categoria)
        messages.success(request, f"Voto registrado em {candidato.usuario.nome} ({categoria.titulo}).")

    return redirect("pagina_votacao")

    return redirect("pagina_votacao")
@login_required
def sair(request):
    logout(request)
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('login')


