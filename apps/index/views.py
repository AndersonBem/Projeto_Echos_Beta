from django.shortcuts import render,redirect, get_object_or_404
from apps.index.models import Veterinario, Clinica, Paciente, Tutor, LaudosPadrao, Frases, Laudo
from django.contrib import messages
from apps.index.forms import VeterinarioForms, ClinicaForms, PacienteForms, TutorForms, PacienteCaninoForms, LaudoForms, RacaFelinoForms, RacaCaninoForms, LaudoPadraoForms, FrasesForm
from apps.index.mixins import ConfirmacaoMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
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

def lista_frases(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    frases = Frases.objects.all()
    return render(request, 'index/lista_frases.html', {"frases": frases})

def lista_laudos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    lista_laudos = LaudosPadrao.objects.all()
    return render(request, 'index/lista_laudos.html', {"lista_laudos": lista_laudos})


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
    clinica_nome = clinica.nome
    params = f"?buscar={clinica_nome.replace(' ', '+')}"
    url = reverse('buscar_clinica')
    if request.method == 'POST':
        form = ClinicaForms(request.POST, request.FILES, instance=clinica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliníca alterada')
            
            return redirect(url + params)
    return render (request, 'index/editar/editar_clinica.html', {'form':form, 'clinica_id': clinica_id})

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
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))
    return render (request, 'index/editar/editar_paciente.html', {'form':form, 'paciente_id': paciente_id})

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
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))
    return render (request, 'index/editar/editar_paciente_canino.html', {'form':form, 'paciente_id': paciente_id})

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
            return redirect(reverse('exibicao_tutor', kwargs={'tutor_id': tutor_id}))
    return render (request, 'index/editar/editar_tutor.html', {'form':form, 'tutor_id': tutor_id})

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
    veterinario_nome = veterinario.nome
    params = f"?buscar={veterinario_nome.replace(' ', '+')}"
    url = reverse('buscar_veterinario')
    if request.method == 'POST':
        form=VeterinarioForms(request.POST, request.FILES, instance=veterinario)
        if form.is_valid():
            form.save()
            messages.success(request, "Veterinário salvo")
            return redirect(url + params)
    return render(request, 'index/editar/editar_veterinario.html', {'form': form, 'veterinario_id': veterinario_id})

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
    
    return render (request, "index/busca/buscar_paciente.html", {"pacientes":pacientes} )

def buscar_veterinario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    veterinarios = Veterinario.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            veterinarios = veterinarios.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_veterinario.html", {"veterinarios":veterinarios} )

def buscar_tutor(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    tutores = Tutor.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            tutores = tutores.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_tutor.html", {"tutores":tutores} )

def buscar_clinica(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    clinicas = Clinica.objects.order_by("nome").all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            clinicas = clinicas.filter(nome__unaccent__icontains=nome_a_buscar)

    return render (request, "index/busca/buscar_clinica.html", {"clinicas":clinicas} )


def selecao(request, tutor_id):
    return render(request, 'index/selecao.html', {'tutor_id': tutor_id})



def exibicao(request, paciente_id):
    # Buscar o paciente pelo ID, retornar 404 se não encontrado
    paciente = Paciente.objects.get(id=paciente_id)
    laudo = LaudosPadrao.objects.all()
    laudos_paciente = paciente.laudos.all()
    # Agora, você pode passar o objeto do paciente para o template
    return render(request, 'index/exibir/exibicao.html', {'paciente': paciente, 'laudo':laudo, 'laudos_paciente':laudos_paciente})

def exibicao_tutor(request, tutor_id):
    # Buscar o paciente pelo ID, retornar 404 se não encontrado
    tutor = Tutor.objects.get(id=tutor_id)

    # Agora, você pode passar o objeto do paciente para o template
    return render(request, 'index/exibir/exibicao_tutor.html', {'tutor': tutor})


def laudo(request, paciente_id, tutor_id, laudo_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    frases = Frases.objects.all()

    try:
        paciente = Paciente.objects.select_related('tutor').get(id=paciente_id)
        tutor = Tutor.objects.get(id=tutor_id)
        laudopadrao = LaudosPadrao.objects.get(id=laudo_id)
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
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))
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
            'tipo_laudo': laudopadrao,
            'laudo': laudopadrao.laudo,
            
        })

    return render(request, 'index/laudo.html', {'form': form, 'paciente': paciente, 'tutor': tutor, 'frases':frases})

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
            return redirect('lista_laudos')
    return render(request,'index/cadastrar_laudo.html', {'form':form})


def escolha_exame(request):
    laudo = LaudosPadrao.objects.all()
    return render(request, 'index/escolha_exame.html', {'laudo': laudo})

def obter_frases(request):
    frases = Frases.objects.values('tipo', 'palavra_chave', 'texto')
    return JsonResponse({'frases': list(frases)})

def nova_frase(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    form = FrasesForm
    if request.method == 'POST':
        form = FrasesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova frase Cadastrada')
            return redirect('lista_pacientes')
    return render(request,'index/nova_frase.html', {'form':form})


def editar_frases(request, frases_id):
    frases = Frases.objects.get(id=frases_id)
    form = FrasesForm(instance=frases)
    if request.method == 'POST':
        form = FrasesForm(request.POST, request.FILES, instance=frases)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frase alterado')
            return redirect('lista_frases')
    return render (request, 'index/editar/editar_frases.html', {'form':form, 'frases_id': frases_id})

@method_decorator(require_POST, name='dispatch')
class DeletarFraseView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_frases'

    def get(self, request, pk):
        frases = get_object_or_404(Frases, pk=pk)
        return render(request, self.template_name, {'frases': frases})

    def post(self, request, pk):
        frases = get_object_or_404(Frases, pk=pk)
        frases.delete()
        return redirect(self.success_url)

def deletar_frase(request, frases_id):
    frases = Frases.objects.get(id=frases_id)
    frases.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_frases')


@method_decorator(require_POST, name='dispatch')
class DeletarLaudosPadraoView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_laudos'

    def get(self, request, pk):
        laudospadrao = get_object_or_404(LaudosPadrao, pk=pk)
        return render(request, self.template_name, {'laudospadrao': laudospadrao})

    def post(self, request, pk):
        laudospadrao = get_object_or_404(LaudosPadrao, pk=pk)
        laudospadrao.delete()
        return redirect(self.success_url)

def deletar_laudospadrao(request, laudo_id):
    laudo = LaudosPadrao.objects.get(id=laudo_id)
    laudo.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect('lista_laudos')





def exibir_laudo(request,laudos_paciente_id):
    laudo_paciente = Laudo.objects.get(id=laudos_paciente_id)
    return render(request, 'index/exibir/exibir_laudo.html', {'laudo_paciente': laudo_paciente})


@method_decorator(require_POST, name='dispatch')
class DeletarLaudoView(View):
    template_name = 'confirmacao_deletar.html'
    success_url = 'lista_pacientes'

    def get(self, request, pk):
        laudo_paciente = get_object_or_404(laudo_paciente, pk=pk)
        return render(request, self.template_name, {'laudo_paciente': laudo_paciente})

    def post(self, request, pk):
        laudo_paciente = get_object_or_404(Laudo, pk=pk)
        laudo.delete()
        return redirect(self.success_url)

def deletar_laudo(request, laudo_paciente_id):
    laudo = Laudo.objects.get(id=laudo_paciente_id)
    paciente_id = laudo.paciente.id
    laudo.delete()
    messages.success(request, 'Deleção feita com sucesso')
    return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))

def editar_laudo(request, laudo_paciente_id):
    laudo_paciente = Laudo.objects.get(id=laudo_paciente_id)
    form = LaudoForms(instance=laudo_paciente)

    if request.method == 'POST':
        form=LaudoForms(request.POST, request.FILES, instance=laudo_paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Laudo salvo")
            return redirect(reverse('exibir_laudo', kwargs={'laudos_paciente_id': laudo_paciente_id}))
    return render(request, 'index/editar/editar_laudo.html', {'form': form, 'laudo_paciente': laudo_paciente})


def editar_laudopadrao(request, laudo_id):
    
    laudo = get_object_or_404(LaudosPadrao, id=laudo_id)
    form = LaudoPadraoForms(instance=laudo)
    if request.method == 'POST':
        form = LaudoPadraoForms(request.POST, request.FILES, instance=laudo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laudo padrão alterado')
            return redirect('lista_laudos')
    return render (request, 'index/editar/editar_laudopadrao.html', {'form':form, 'laudo_id': laudo_id})





