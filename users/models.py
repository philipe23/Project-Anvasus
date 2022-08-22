from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from localflavor.br.models import BRCPFField


# Create your models here.


# Calculadora de idade para o Professor.
def age(birthdate):
    today = date.today()
    idade = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return idade


# Definição do CustomAccountManager.
class CustomAccountManager(BaseUserManager):

    # SuperUser.
    def create_superuser(self, cpf, nome, nascimento, titulacao, password, **other_fields):

        # Padrões para o SuperUser.
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Validações.
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ser designado como staff')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ser designado como superuser')

        if other_fields.get('is_active') is not True:
            raise ValueError('Superuser precisa ser designado como ativo')

        return self.create_user(cpf, nome, nascimento, titulacao, password, **other_fields)

    # User.
    def create_user(self, cpf, nome, nascimento, titulacao, password, **other_fields):

        # Validações.
        if not cpf:
            raise ValueError('Você precisa inserir um CPF')

        if not nome:
            raise ValueError('Você precisa inserir um nome')

        if not nascimento:
            raise ValueError('Você precisa inserir uma data de nascimento')

        if not titulacao:
            raise ValueError('Você precisa inserir uma titulação')

        user = self.model(cpf=cpf, nome=nome, nascimento=nascimento, titulacao=titulacao, **other_fields)
        user.set_password(password)
        user.save()
        return user


# Definição do Professor.
class Professor(AbstractBaseUser, PermissionsMixin):
    TITULACAO = (
        ('Graduação', 'Graduação'),
        ('Especialização', 'Especialização'),
        ('Mestrado', 'Mestrado'),
        ('Doutorado', 'Doutorado')
    )
    nome = models.CharField(verbose_name="Nome", max_length=255)
    cpf = BRCPFField(verbose_name="CPF", max_length=14, unique=True)
    nascimento = models.DateField(verbose_name="Data de nascimento")
    titulacao = models.CharField(
        verbose_name="Titulação", help_text="Obrigatório. Insira seu nível de graduação",
        max_length=14, choices=TITULACAO
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()
    termos = models.BooleanField(null=False, blank=False, default=True)

    USERNAME_FIELD = 'cpf'

    REQUIRED_FIELDS = ['nome', 'nascimento', 'titulacao']

    # Funções úteis.
    def __str__(self):
        return self.nome

    def get_nome(self):
        return self.nome

    def get_nascimento(self):
        return self.nascimento

    def get_idade(self):
        idade = age(self.nascimento)
        return idade

    def get_cpf(self):
        return self.cpf

    def get_id(self):
        return self.id

    def get_cursos(self):
        return Curso.objects.filter(professor=self).all()

    def get_quant_cursos(self):
        return Curso.objects.filter(professor=self).count()


# Definição do Tema.
class Tema(models.Model):
    nome = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nome


# Definição do Curso.
class Curso(models.Model):
    STATUS = (
        ('Aprovado', 'Aprovado'),
        ('Pendente', 'Pendente'),
        ('Recusado', 'Recusado'),
    )
    AVALIACAO = (
        ('Prova', 'Prova'),
        ('Trabalho', 'Trabalho'),
        ('Projeto', 'Projeto'),
    )
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=120, unique=True)
    duracao = models.IntegerField()
    status = models.CharField(max_length=120, default='Pendente', choices=STATUS)
    ementa = models.TextField(max_length=500)
    objetivo = models.TextField(max_length=500)
    avaliacao = models.TextField(max_length=500, choices=AVALIACAO)
    criado = models.DateField(auto_now_add=True, editable=False)
    codigo = models.CharField(max_length=20, null=True, blank=True)

    # Funções úteis.
    def get_quant_topicos(self):
        return Topico.objects.filter(curso=self).count()

    def get_id_professor(self):
        identificacao = Professor.objects.get(curso=self).id
        return identificacao

    def get_nome_professor(self):
        nome = Professor.objects.get(curso=self).nome
        return nome

    def __str__(self):
        return self.titulo


# Definição do tópico.
class Topico(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.titulo

    def get_id_curso(self):
        identificacao = Curso.objects.get(topico=self).id
        return identificacao
