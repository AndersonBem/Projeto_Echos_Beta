from django.shortcuts import render,redirect
from apps.index.models import Veterinario, Clinica, Paciente, Tutor 
from django.contrib import messages
from apps.index.forms import VeterinarioForms, ClinicaForms, PacienteForms, TutorForms


# lista de funções de listas

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    return render(request, 'index/index.html')

def lista_veterinarios(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    veterinarios = Veterinario.objects.order_by("nome").all()
    return render(request, 'index/lista_veterinarios.html', {"veterinarios": veterinarios})

def lista_clinicas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    clinicas = Clinica.objects.order_by("nome").all()
    return render(request,'index/lista_clinicas.html', {"clinicas": clinicas})

def lista_pacientes(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    pacientes = Paciente.objects.order_by("nome").all()
    return render(request, 'index/lista_pacientes.html', {"pacientes": pacientes})

def lista_tutores(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    tutores = Tutor.objects.order_by("nome").all()
    return render(request, 'index/lista_tutores.html', {"tutores": tutores})

#Lista de funções de novo

def nova_clinica(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = ClinicaForms
    if request.method == 'POST':
        form = ClinicaForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova cliníca cadastrada')
            return redirect('lista_clinicas')
    return render(request,'index/nova_clinica.html', {'form':form})

def editar_clinica(request, clinica_id):
    clinica = Clinica.objects.get(id=clinica_id)
    form = ClinicaForms(instance=clinica)

    if request.method == 'POST':
        form = ClinicaForms(request.POST, request.FILES, instance=clinica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliníca alterada')
            return redirect('lista_clinicas')
    return render (request, 'index/editar_clinica.html', {'form':form, 'clinica_id': clinica_id})

def deletar_clinica(request, clinica_id):
    clinica = Clinica.objects.get(id=clinica_id)
    clinica.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_clinicas')

def novo_paciente(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = PacienteForms
    if request.method == 'POST':
        form = PacienteForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Paciente Cadastrado')
            return redirect('lista_pacientes')
    return render(request,'index/novo_paciente.html', {'form':form})

def editar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    form = PacienteForms(instance=paciente)

    if request.method == 'POST':
        form = PacienteForms(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente alterado')
            return redirect('lista_pacientes')
    return render (request, 'index/editar_paciente.html', {'form':form, 'paciente_id': paciente_id})

def deletar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    paciente.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_pacientes')

def novo_tutor(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = TutorForms
    if request.method == 'POST':
        form = TutorForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo tutor cadastrado')
            return redirect('lista_tutores')
    return render(request,'index/novo_tutor.html', {'form': form})

def editar_tutor(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    form = TutorForms(instance=tutor)

    if request.method == 'POST':
        form = TutorForms(request.POST, request.FILES, instance=tutor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutor alterado')
            return redirect('lista_tutores')
    return render (request, 'index/editar_tutor.html', {'form':form, 'tutor_id': tutor_id})


def deletar_tutor(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    tutor.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_tutores')

def novo_veterinario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    form = VeterinarioForms
    if request.method == 'POST':
        form = VeterinarioForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo veterinário Cadastrado')
            return redirect('lista_veterinarios')
    return render(request,'index/novo_veterinario.html', {'form':form})

def editar_veterinario(request, veterinario_id):
    veterinario = Veterinario.objects.get(id=veterinario_id)
    form = VeterinarioForms(instance=veterinario)

    if request.method == 'POST':
        form=VeterinarioForms(request.POST, request.FILES, instance=veterinario)
        if form.is_valid():
            form.save()
            messages.success(request, "Veterinário salvo")
            return redirect('lista_veterinarios')
    return render(request, 'index/editar_veterinario.html', {'form': form, 'veterinario_id': veterinario_id})

def deletar_veterinario(request, veterinario_id):
    veterinario = Veterinario.objects.get(id=veterinario_id)
    veterinario.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_veterinarios')
    

# lista de funções de busca

def buscar_paciente(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    pacientes = Paciente.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            pacientes = pacientes.filter(nome__unaccent__icontains=nome_a_buscar)
    
    return render (request, "index/buscar_paciente.html", {"pacientes":pacientes} )

def buscar_veterinario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    veterinarios = Veterinario.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            veterinarios = veterinarios.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/buscar_veterinario.html", {"veterinarios":veterinarios} )

def buscar_tutor(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    tutores = Tutor.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            tutores = tutores.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/buscar_tutor.html", {"tutores":tutores} )

def buscar_clinica(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    clinicas = Clinica.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            clinicas = clinicas.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/buscar_clinica.html", {"clinicas":clinicas} )
