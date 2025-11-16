from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ("votante", "Votante"),
        ("candidato", "Candidato"),
        ("admin", "Administrador"),
    )

    username = None
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default="votante"
    )
    foto = models.ImageField(upload_to="usuarios/fotos/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "sobrenome"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.tipo})"

    @property
    def pode_votar(self):
        return self.tipo == "votante"

class Categoria(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    icone = models.CharField(
        max_length=10,
        help_text="Coloque aqui o emoji ou código do ícone (ex: 🎨, 📚, ⚽)"
    )
    descricao = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.icone} {self.titulo}"



class Candidato(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={"tipo": "candidato"}
    )
    categoria = models.ForeignKey(
        Categoria,
        related_name="candidatos",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.usuario.nome} - {self.categoria.titulo}"

    @property
    def votos_totais(self):
        """Conta quantos votos esse candidato recebeu"""
        return self.votos.count()



class Voto(models.Model):
    votante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={"tipo": "votante"}
    )
    candidato = models.ForeignKey(
        Candidato,
        related_name="votos",
        on_delete=models.CASCADE
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("votante", "categoria")

    def __str__(self):
        return f"{self.votante.nome} votou em {self.candidato.usuario.nome} ({self.categoria.titulo})"

