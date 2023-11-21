from django.shortcuts import render
from index.models import Veterinario, Clinica, Paciente, Tutor 


# lista de funções de listas

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

#Lista de funções de novo

def nova_clinica(request):
    return render(request,'index/nova_clinica.html')

def novo_paciente(request):
    return render(request,'index/novo_paciente.html')

def novo_tutor(request):
    return render(request,'index/novo_tutor.html')

def novo_veterinario(request):
    return render(request,'index/novo_veterinario.html')

# lista de funções de busca

def buscar_paciente(request):
    
    pacientes = Paciente.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            pacientes = pacientes.filter(nome__unaccent__icontains=nome_a_buscar)
    
    return render (request, "index/busca/buscar_paciente.html", {"pacientes":pacientes} )

def buscar_veterinario(request):

    veterinarios = Veterinario.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            veterinarios = veterinarios.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_veterinario.html", {"veterinarios":veterinarios} )

def buscar_tutor(request):
    
    tutores = Tutor.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            tutores = tutores.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_tutor.html", {"tutores":tutores} )

def buscar_clinica(request):
    
    clinicas = Clinica.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            clinicas = clinicas.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_clinica.html", {"clinicas":clinicas} )
