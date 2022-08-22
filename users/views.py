from .forms import *
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import random
import string


# Create your views here.


# View para registro de Users.
def registerPage(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            login(request, account, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('confirmacao')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html', context)


# Confirmação de registro.
def confirmacao(request):
    return render(request, 'users/confirmacao.html')


# View para login.
def loginPage(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            cpf = request.POST['cpf']
            password = request.POST['password']
            user = authenticate(cpf=cpf, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'users/login.html', context)


# View para logout.
def logoutPage(request):
    logout(request)
    return redirect('home')


# View para vizualizar conta.
def accountView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        context = {}
        return render(request, 'users/account.html', context)


# View para vizualizar Curso.
def courseView(request, pk):

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        course = Curso.objects.get(id=pk)
        topics = Curso.objects.get(id=pk).topico_set.all()
        context = {'course': course, 'topics': topics}
        return render(request, 'users/course.html', context)


# View para vizualizar Tópico.
def topicView(request, pk):

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        topic = Topico.objects.get(id=pk)
        context = {'topic': topic}
        return render(request, 'users/topic.html', context)


# View para registrar Tópico.
def topicRegister(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        curso = Curso.objects.get(id=pk)
        form = TopicForm(initial={'curso': curso})
        if request.method == 'POST':
            print('Printing POST: ', request.POST)
            form = TopicForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/course/%s' % pk)
        context = {'form': form, 'curso': curso}
        return render(request, 'users/topic_register.html', context)


# View para deletar Tópico.
def topicDelete(request, pk, pk2):
    curso = Curso.objects.get(id=pk2)
    topic = Topico.objects.get(id=pk)
    if request.method == 'POST':
        topic.delete()
        return redirect('/course/%s' % pk2)
    context = {'topic': topic, 'curso': curso}
    return render(request, 'users/topic_delete.html', context)


# View para registrar Curso.
def courseRegister(request, pk):
    teacher = Professor.objects.get(id=pk)
    form = CourseForm(initial={'professor': teacher, 'status': "Pendente"})
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        print(request.method)
    context = {'form': form, 'teacher': teacher}
    return render(request, 'users/course_register.html', context)


# View para atualizar Cursos.
def courseUpdate(request, pk):
    course = Curso.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user.nome
            form.save()
            return redirect('/course/%s' % pk)
    context = {'form': form}
    return render(request, 'users/course_update.html', context)


# View para deletar Cursos.
def courseDelete(request, pk):
    course = Curso.objects.get(id=pk)
    context = {'course': course}
    if request.method == 'POST':
        course.delete()
        return redirect('/')
    return render(request, 'users/course_delete.html', context)


# View para confirmar emissão de certificado.
def certificado(request, pk, pk2):
    teacher = Professor.objects.get(id=pk)
    course = Curso.objects.get(id=pk2)
    context = {'teacher': teacher, 'course': course}
    return render(request, 'users/certificado.html', context)


# Definição de função auxiliar (gerar código aleatório).
def get_code(length):
    letras = string.ascii_lowercase
    code = ''.join(random.choice(letras) for i in range(length))
    return code


# View para gerar PDF.
def pdf(request, pk, pk2):
    teacher = Professor.objects.get(id=pk)
    course = Curso.objects.get(id=pk2)
    tema = str(course.tema)
    carga = str(course.duracao)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    identifier = get_code(10)
    course.codigo = identifier
    course.save()
    p = canvas.Canvas(response)

    p.drawString(100, 800, "Certificado De Curso Ministrado")
    p.drawString(100, 750, "Nome Do Professor: " + teacher.nome)
    p.drawString(100, 700, "CPF Do Professor: " + teacher.cpf)
    p.drawString(100, 650, "Título Do Curso: " + course.titulo)
    p.drawString(100, 600, "Tema Do Curso: " + tema)
    p.drawString(100, 550, "Carga Horária: " + carga)
    p.drawString(100, 500, "Data De Geração Do Certificado: " + ts)
    p.drawString(100, 450, "Identificador: " + identifier)

    imagem = ImageReader('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOdS5aeYM4_909ivDADoISVo3dRmFcz8p26RQsbBylgyNMfWm7e63kLBOu_dbqteA076Y&usqp=CAU')
    p.drawImage(imagem, 200, 100, mask='auto')

    p.showPage()
    p.save()

    return response


# View principal.
def home(request):
    context = {}
    return render(request, 'users/home.html', context)
