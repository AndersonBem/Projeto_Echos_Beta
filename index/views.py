from django.shortcuts import render
from index.models import Veterinario, Clinica, Paciente, Tutor 


# Create your views here.

def index(request):
    return render(request, 'index/index.html')

def lista_veterinarios(request):
    veterinarios = Veterinario.objects.order_by("nome").all()
    return render(request, 'index/lista_veterinarios.html', {"veterinarios": veterinarios})

def lista_clinicas(request):
    clinicas = Clinica.objects.order_by("nome").all()
    return render(request,'index/lista_clinicas.html', {"clinicas": clinicas})

def lista_pacientes(request):
    pacientes = Paciente.objects.order_by("nome").all()
    return render(request, 'index/lista_pacientes.html', {"pacientes": pacientes})

def lista_tutores(request):
    tutores = Tutor.objects.order_by("nome").all()
    return render(request, 'index/lista_tutores.html', {"tutores": tutores})

def nova_clinica(request):
    return render(request,'index/nova_clinica.html')

def novo_paciente(request):
    return render(request,'index/novo_paciente.html')

def novo_tutor(request):
    return render(request,'index/novo_tutor.html')

def novo_veterinario(request):
    return render(request,'index/novo_veterinario.html')