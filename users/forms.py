from .models import *
from django import forms
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from localflavor.br.forms import BRCPFField


# Forms para cadastro de Users.
class RegistrationForm(UserCreationForm):
    cpf = BRCPFField(widget=forms.TextInput(attrs={'data-mask': '000.000.000-00'}), label='CPF', max_length=14, help_text='Obrigatório. Insira seu CPF')
    nome = forms.CharField(label='Nome completo', help_text='Obrigatório. Insira seu nome completo')
    nascimento = forms.DateField(
        label="Data de nascimento", help_text='Obrigatório.',
        widget=NumberInput(attrs={'type': 'date'})
    )
    termos = forms.BooleanField(required=True, label='Eu li e aceito os termos de uso', initial=False)

    class Meta:
        model = Professor
        fields = ['cpf', 'nome', 'nascimento', 'titulacao', 'password1', 'password2', 'termos']

    # Validação da data de nascimento
    def clean_nascimento(self):
        nascimento = self.cleaned_data.get("nascimento")
        if nascimento.year > 2005:
            raise forms.ValidationError("Sua idade precisa ser maior que 18")
        return nascimento


# Forms para login.
class AccountAuthenticationForm(forms.ModelForm):
    cpf = BRCPFField(widget=forms.TextInput(attrs={'data-mask': '000.000.000-00'}), label='CPF', max_length=14, help_text='Formato 000.000.000-00')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ('cpf', 'password')

    def clean(self):
        if self.is_valid():
            cpf = self.cleaned_data['cpf']
            password = self.cleaned_data['password']
            if not authenticate(cpf=cpf, password=password):
                raise forms.ValidationError("Informações inválidas")


# Forms para Tópicos de Aula.
class TopicForm(ModelForm):
    class Meta:
        model = Topico
        fields = '__all__'


# Forms para Cursos (registrar, apagar e deletar)
class CourseForm(forms.ModelForm):
    titulo = forms.CharField(label="Título", max_length=120)
    duracao = forms.IntegerField(label="Carga Horária")
    status = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    ementa = forms.CharField(label="Ementa", max_length=500)
    objetivo = forms.CharField(label="Objetivo Geral", max_length=500)

    class Meta:
        model = Curso
        fields = ('professor', 'tema', 'titulo', 'duracao', 'ementa', 'objetivo', 'avaliacao', 'status')

    def clean_duracao(self):
        duracao = self.cleaned_data.get("duracao")
        if duracao < 3 or duracao > 350:
            raise forms.ValidationError("Insira um número entre 3 e 350")
        return duracao
