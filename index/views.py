from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index/index.html')

def lista_veterinarios(request):
    return render(request, 'index/lista_veterinarios.html')

def lista_clinicas(request):
    return render(request,'index/lista_clinicas.html')

def lista_pacientes(request):
    return render(request, 'index/lista_pacientes.html')

def lista_tutores(request):
    return render(request, 'index/lista_tutores.html')

def nova_clinica(request):
    return render(request,'index/nova_clinica.html')

def novo_paciente(request):
    return render(request,'index/novo_paciente.html')

def novo_tutor(request):
    return render(request,'index/novo_tutor.html')

def novo_veterinario(request):
    return render(request,'index/novo_veterinario.html')