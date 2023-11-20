from django.shortcuts import render,redirect, get_object_or_404
from apps.index.models import Veterinario, Clinica, Paciente, Tutor, LaudosPadrao
from django.contrib import messages
from apps.index.forms import VeterinarioForms, ClinicaForms, PacienteForms, TutorForms, PacienteCaninoForms, LaudoForms, RacaFelinoForms, RacaCaninoForms, LaudoPadraoForms
from apps.index.mixins import ConfirmacaoMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
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
    pacientes= Paciente.objects.order_by("nome").all()
    return render(request, 'index/lista_pacientes.html', {"pacientes": pacientes})

def lista_tutores(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    tutores = Tutor.objects.exclude(nome='Sem tutor').order_by("nome").all()
    return render(request, 'index/lista_tutores.html', {"tutores": tutores})

#Lista de funções de novo
#Clinica
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

@method_decorator(require_POST, name='dispatch')
class DeletarClinicaView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_clinicas'

    def get(self, request, pk):
        clinica = get_object_or_404(Clinica, pk=pk)
        return render(request, self.template_name, {'clinica': clinica})

    def post(self, request, pk):
        clinica = get_object_or_404(Clinica, pk=pk)
        clinica.delete()
        return redirect(self.success_url)

def deletar_clinica(request, clinica_id):
    clinica = Clinica.objects.get(id=clinica_id)
    clinica.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_clinicas')

#pacientes felinos

def novo_paciente(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    tutor_id = request.GET.get('tutor_id')
    ultimo_tutor = Tutor.objects.last()

    tutor_inicial = get_object_or_404(Tutor, id=tutor_id) if tutor_id else ultimo_tutor

    form = PacienteForms(request.POST or None, initial={'tutor': tutor_inicial})

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Paciente Cadastrado')
            return redirect('lista_pacientes')

    return render(request, 'index/novo_paciente.html', {'form': form})


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

@method_decorator(require_POST, name='dispatch')
class DeletarPacienteView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_pacientes'

    def get(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        return render(request, self.template_name, {'paciente': paciente})

    def post(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)
        paciente.delete()
        return redirect(self.success_url)

def deletar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    paciente.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_pacientes')

#pacientes Caninos

def novo_paciente_canino(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    tutor_id = request.GET.get('tutor_id')
    ultimo_tutor = Tutor.objects.last()

    tutor_inicial = get_object_or_404(Tutor, id=tutor_id) if tutor_id else ultimo_tutor

    form = PacienteCaninoForms(request.POST or None, initial={'tutor': tutor_inicial})

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Paciente Canino Cadastrado')
            return redirect('lista_pacientes')

    return render(request, 'index/novo_paciente_canino.html', {'form': form})

def editar_paciente_canino(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    form = PacienteCaninoForms(instance=paciente)

    if request.method == 'POST':
        form = PacienteCaninoForms(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente alterado')
            return redirect('lista_pacientes')
    return render (request, 'index/editar_paciente_canino.html', {'form':form, 'paciente_id': paciente_id})

def deletar_paciente_canino(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    paciente.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_pacientes')

#tutores

def novo_tutor(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    form = TutorForms
    if request.method == 'POST':
        form = TutorForms(request.POST)
        if form.is_valid():
            novo_tutor = form.save()  # Salva o novo tutor e obtém a instância
            messages.success(request, 'Novo tutor cadastrado')
            return redirect('exibicao_tutor', tutor_id=novo_tutor.id)
    
    return render(request, 'index/novo_tutor.html', {'form': form})
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

@method_decorator(require_POST, name='dispatch')
class DeletarTutorView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_tutores'

    def get(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        return render(request, self.template_name, {'tutor': tutor})

    def post(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        tutor.delete()
        return redirect(self.success_url)

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

@method_decorator(require_POST, name='dispatch')
class DeletarVeterinarioView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_veterinarios'

    def get(self, request, pk):
        veterinario = get_object_or_404(Veterinario, pk=pk)
        return render(request, self.template_name, {'veterinario': veterinario})

    def post(self, request, pk):
        veterinario = get_object_or_404(Veterinario, pk=pk)
        veterinario.delete()
        return redirect(self.success_url)

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


def selecao(request, tutor_id):
    return render(request, 'index/selecao.html', {'tutor_id': tutor_id})



def exibicao(request, paciente_id):
    # Buscar o paciente pelo ID, retornar 404 se não encontrado
    paciente = Paciente.objects.get(id=paciente_id)

    # Agora, você pode passar o objeto do paciente para o template
    return render(request, 'index/exibicao.html', {'paciente': paciente})

def exibicao_tutor(request, tutor_id):
    # Buscar o paciente pelo ID, retornar 404 se não encontrado
    tutor = Tutor.objects.get(id=tutor_id)

    # Agora, você pode passar o objeto do paciente para o template
    return render(request, 'index/exibicao_tutor.html', {'tutor': tutor})


def laudo(request, paciente_id, tutor_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    try:
        paciente = Paciente.objects.select_related('tutor').get(id=paciente_id)
        tutor = Tutor.objects.get(id=tutor_id)
    except (Paciente.DoesNotExist, Tutor.DoesNotExist):
        messages.error(request, "Paciente ou Tutor não encontrado")
        return redirect('alguma_pagina_de_erro')

    if request.method == 'POST':
        form = LaudoForms(request.POST)
        if form.is_valid():
            form.instance.paciente = paciente
            form.instance.tutor = tutor
            # Preencha outros campos conforme necessário

            form.save()
            messages.success(request, 'Laudo salvo com sucesso')
            return redirect('lista_pacientes')  # Altere para a URL desejada após salvar o laudo
        else:
            messages.error(request, 'Erro ao salvar o laudo. Por favor, verifique os campos.')
    else:
        form = LaudoForms(initial={
            'paciente': paciente,
            'especie': paciente.especie,
            'raca': paciente.raca,
            'sexo': paciente.sexo,
            'tutor': tutor,
            'email': tutor.email,
            'idade': paciente.idade,
            'peso': paciente.peso,
        })

    return render(request, 'index/laudo.html', {'form': form, 'paciente': paciente, 'tutor': tutor})

#Criação de novas raças

def nova_raca_felino(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = RacaFelinoForms
    if request.method == 'POST':
        form = RacaFelinoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova raça Cadastrada')
            return redirect('novo_paciente')
    return render(request,'index/nova_raca_felino.html', {'form':form})

def nova_raca_canino(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = RacaCaninoForms
    if request.method == 'POST':
        form = RacaCaninoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova raça Cadastrada')
            return redirect('novo_paciente_canino')
    return render(request,'index/nova_raca_canino.html', {'form':form})

def cadastrar_laudo(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = LaudoPadraoForms
    if request.method == 'POST':
        form = LaudoPadraoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laudo cadastrado')
            return redirect('lista_pacientes')
    return render(request,'index/cadastrar_laudo.html', {'form':form})


def escolha_exame(request):
    laudo = LaudosPadrao.objects.all()
    return render(request, 'index/escolha_exame.html', {'laudo': laudo})