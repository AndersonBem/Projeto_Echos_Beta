from django.shortcuts import render,redirect, get_object_or_404
from apps.index.models import Veterinario, Clinica, Paciente, Tutor, LaudosPadrao, Frases, Laudo, LaudoImagem, Inventario, FormaDePagamento
from django.contrib import messages
from apps.index.forms import VeterinarioForms, ClinicaForms, PacienteForms, TutorForms, PacienteCaninoForms, LaudoForms, RacaFelinoForms, RacaCaninoForms, LaudoPadraoForms, FrasesForm,\
NovaImagemForm, RelatorioForm
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.template.loader import render_to_string, get_template
import tempfile
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
import tempfile
from django.template.loader import render_to_string  
import weasyprint
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date
#agendamento -email
from django.conf import settings
from django_q.tasks import async_task
from .tasks import enviar_pdf_task
from datetime import datetime, timedelta
from django_q.tasks import schedule
from django.utils import timezone
import asyncio
from django_q.tasks import Schedule
from django import forms
# lista de funções de listas
from django.utils.decorators import decorator_from_middleware
from django.middleware.csrf import CsrfViewMiddleware
import os
import io
import boto3
from botocore.exceptions import NoCredentialsError
from django.db.models import Count
from django.http import HttpResponseServerError
from zipfile import ZipFile
from io import BytesIO
from urllib.parse import unquote




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
    frases = Frases.objects.order_by("palavra_chave").all()
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
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
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
            paciente = form.save()
            paciente_id = paciente.id
            messages.success(request, 'Novo Paciente Cadastrado')
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))

    return render(request, 'index/novo_paciente.html', {'form': form})


def editar_paciente(request, paciente_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
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
            paciente = form.save()
            paciente_id = paciente.id
            messages.success(request, 'Novo Paciente Canino Cadastrado')
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))

    return render(request, 'index/novo_paciente_canino.html', {'form': form})

def editar_paciente_canino(request, paciente_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
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
    
    pacientes = Paciente.objects.all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            pacientes = pacientes.filter(nome__unaccent__icontains=nome_a_buscar)
    # Ordena os pacientes por nome após o filtro de busca
    pacientes = pacientes.order_by("nome", "tutor__nome")
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
        form = LaudoForms(request.POST, request.FILES)
        if form.is_valid():
            form.instance.paciente = paciente
            form.instance.tutor = tutor
            # Preencha outros campos conforme necessário

            laudo_imagem = form.save()
            files = request.FILES.getlist('laudo_imagem')
            if files:
                for f in files:
                    LaudoImagem.objects.create(
                        laudo=laudo_imagem,
                        image=f
                    )
            messages.success(request, 'Laudo salvo com sucesso')
            # Agora, após salvar o laudo, obtenha o ID corretamente antes de redirecionar
            laudo_id = laudo_imagem.id

            # Redirecione para a página de transição
            return render(request, 'index/laudo.html', {'form': None, 'paciente': paciente, 'tutor': tutor, 'frases': frases, 'transicao': True, 'laudo_id': laudo_id})
        else:
            messages.error(request, 'Erro ao salvar o laudo. Por favor, verifique os campos.')
            print(form.errors)  # Adicione esta linha para imprimir os erros no console
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
            return redirect('lista_frases')
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
    laudo_paciente = get_object_or_404(Laudo, id=laudos_paciente_id)
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
            laudo_imagem = form.save()
            files = request.FILES.getlist('laudo_imagem')
            if files:
                for f in files:
                    LaudoImagem.objects.create(
                        laudo=laudo_imagem,
                        image=f
                    )
            messages.success(request, "Laudo salvo")
            # Agora, após salvar o laudo, obtenha o ID corretamente antes de redirecionar
            laudo_id = laudo_imagem.id

            # Redirecione para a página de transição
            return render(request, 'index/laudo.html', {'form': None, 'transicao': True, 'laudo_id': laudo_id})
    return render(request, 'index/editar/editar_laudo.html', {'form': form, 'laudo_paciente': laudo_paciente})

def auto_save_laudo(request, laudo_paciente_id):
    laudo_paciente = Laudo.objects.get(id=laudo_paciente_id)
    form = LaudoForms(instance=laudo_paciente)
    if request.method == 'POST':
        
        form=LaudoForms(request.POST, request.FILES, instance=laudo_paciente)
        if form.is_valid():
            laudo = Laudo.objects.get(id=laudo_paciente_id)  # Obtenha a instância do banco de dados
            form = LaudoForms(request.POST, request.FILES, instance=laudo)
            laudo = form.save(commit=False)  # Evitar commit automático
            # Faça qualquer processamento adicional, se necessário
            laudo.save()  # Commit manual
            print("Laudo salvo com sucesso!")
            return JsonResponse({'status': 'success'})
        else:
            print("Formulário inválido:", form.errors)
        return JsonResponse({'status': 'success'})

    # Retorna uma resposta JSON indicando erro se a requisição não for do tipo POST
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})


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


def deletar_imagem(request, imagem_id):
    imagem = get_object_or_404(LaudoImagem, id=imagem_id)
    laudo_id = imagem.laudo.id  # Captura o ID do laudo antes de deletar a imagem
    imagem.delete()
    laudo = Laudo.objects.get(id=laudo_id)

    form = NovaImagemForm()

    return render(request, 'index/adicionar_imagem.html', {'form': form, 'laudo': laudo})

def excluir_todas_imagens(request, laudo_id):
    if request.method == 'POST':
        laudo_imagens = LaudoImagem.objects.filter(laudo_id=laudo_id)
        for imagem in laudo_imagens:
            imagem.delete()

    laudo = Laudo.objects.get(id=laudo_id)

    form = NovaImagemForm()

    return render(request, 'index/adicionar_imagem.html', {'form': form, 'laudo': laudo})


def adicionar_imagem(request, laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    if request.method == 'POST':
        form = NovaImagemForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('laudo_imagem')
            if files:
                for f in files:
                    LaudoImagem.objects.create(
                        laudo=laudo,
                        image=f
                    )
            return render(request, 'index/adicionar_imagem.html', {'form': form, 'laudo': laudo})
    else:
        form = NovaImagemForm()

    return render(request, 'index/adicionar_imagem.html', {'form': form, 'laudo': laudo})





def export_pdf(request, laudos_paciente_id): 
    laudo = Laudo.objects.get(id=laudos_paciente_id)

    # Configurando o link para AWS
    data_atual = laudo.data.strftime("%Y-%m-%d")
    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    s3_filename_format = s3_filename.replace(" ", "+")
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

    # Crie o QR code com o link para AWS
    qr_img = qrcode.make(pdf_link)
    
    # Converta o QR code em BytesIO
    qr_bytes = BytesIO()
    qr_img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)
    
    # Converta o BytesIO em imagem PIL
    qr_pil_img = Image.open(qr_bytes)
    
    # Converta a imagem do QR code em base64
    qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode()
    
    # Adicione a imagem codificada ao contexto
    context = {'laudo': laudo, 'qr_base64': qr_base64}
    
    # Renderize o template com o contexto
    html_index = render_to_string('export-pdf.html', context)  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Laudo - '+str(laudo.tipo_laudo)+' - '+str(laudo.paciente)+' - '+str(laudo.data)+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush() 
        output.seek(0)
        response.write(output.read()) 
    return response

import qrcode
from PIL import Image
from io import BytesIO
import base64
from django.utils.text import slugify

def exibir_pdf(request, laudos_paciente_id):
    laudo = Laudo.objects.get(id=laudos_paciente_id)

    # Configurando o link para AWS
    data_atual = laudo.data.strftime("%Y-%m-%d")
    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    s3_filename_format = s3_filename.replace(" ", "+")
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

    # Crie o QR code com o link para AWS
    qr_img = qrcode.make(pdf_link)
    
    # Converta o QR code em BytesIO
    qr_bytes = BytesIO()
    qr_img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)
    
    # Converta o BytesIO em imagem PIL
    qr_pil_img = Image.open(qr_bytes)
    
    # Converta a imagem do QR code em base64
    qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode()
    
    # Adicione a imagem codificada ao contexto
    context = {'laudo': laudo, 'qr_base64': qr_base64}
    
    # Supondo que 'laudo' seja o objeto que contém o tipo do laudo
    tipo_laudo_slug = slugify(laudo.tipo_laudo)

    
    # Renderize o template com o contexto
    if tipo_laudo_slug == 'usg-abdominal':
        html_index = render_to_string('PDF/export-pdf-usg.html', context)
    if tipo_laudo_slug == 'ecocardiograma':
        html_index = render_to_string('PDF/export-pdf-eco.html', context)
    if tipo_laudo_slug == 'eletrocardiograma':
        html_index = render_to_string('PDF/export-pdf-ecg.html', context)
    if tipo_laudo_slug == 'pressao-arterial':
        html_index = render_to_string('PDF/export-pdf-pressao.html', context)
    if tipo_laudo_slug == 'cistocentese':
        html_index = render_to_string('PDF/export-pdf-cistocentese.html', context)
    if tipo_laudo_slug == 'usg-cervical':
        html_index = render_to_string('PDF/export-pdf-usg-cervical.html', context)
    if tipo_laudo_slug == 'usg-gestacional':
        html_index = render_to_string('PDF/export-pdf-usg-gestacional.html', context)
    if tipo_laudo_slug == 'usg-ocular':
        html_index = render_to_string('PDF/export-pdf-usg-ocular.html', context)            
    
     
    
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Products'+str(laudo.paciente)+str(laudo.data)+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush() 
        output.seek(0)
        response.write(output.read()) 
    return response


def enviar_pdf(request, laudos_paciente_id):
    laudo = Laudo.objects.get(id=laudos_paciente_id)
    

    # Configurar o fuso horário padrão
    utc_minus3 = timezone.get_default_timezone()

    # Obter a hora atual no fuso horário padrão
    now_utc_minus3 = timezone.now().astimezone(utc_minus3)

    # Criar a hora_agendada respeitando o fuso horário padrão
    #hora_agendada = now_utc_minus3.replace(hour=20, minute=00, second=0, microsecond=0)
    hora_agendada = laudo.hora_envio
    
    if now_utc_minus3.replace(tzinfo=None) > hora_agendada.replace(tzinfo=None):
        # Se sim, agendar para amanhã às 20h
        hora_agendada += timedelta(days=1)
    novo_horario = hora_agendada
    while Schedule.objects.filter(next_run=novo_horario):
    # Se sim, adicione 1 minuto ao novo horário
        novo_horario += timezone.timedelta(minutes=5)

    try:
        task = schedule(
            'apps.index.tasks.enviar_pdf_task',
            laudo.id,
            name=f'Email- {laudo.tutor} - {laudo.paciente} -  {laudo.tipo_laudo}',
            schedule_type='O',
            next_run=novo_horario
        )
        messages.success(request, "Tarefa agendada com sucesso")

        # Redirecione para a página de edição de horário com o ID da tarefa
        return redirect('lista_tarefas_agendadas')
    except Exception as e:
        messages.error(request, f"Erro ao agendar tarefa: {str(e)}")
        return redirect('exibicao', paciente_id=laudo.paciente.id)



def lista_tarefas_agendadas(request):
    tarefas_agendadas = Schedule.objects.all()
    laudo =Laudo.objects.all()
    return render(request, 'index/exibir/lista_tarefas_agendadas.html', {'tarefas_agendadas': tarefas_agendadas})

   
def deletar_tarefa(request, tarefa_id):
    tarefa = Schedule.objects.get(id=tarefa_id)
    tarefa.delete()
    return redirect('lista_tarefas_agendadas')


class EditarHorarioForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['next_run']

def editar_horario_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Schedule, id=tarefa_id)

    if request.method == 'POST':
        form = EditarHorarioForm(request.POST, instance=tarefa)
        if form.is_valid():
            # Obtenha o novo horário escolhido pelo usuário
            novo_horario = form.cleaned_data['next_run']

            # Verifique se já existe uma tarefa agendada para o novo horário
            while Schedule.objects.filter(next_run=novo_horario).exclude(id=tarefa.id).exists():
                # Se sim, adicione 1 minuto ao novo horário
                novo_horario += timedelta(minutes=5)

            # Atualize o horário da tarefa
            tarefa.next_run = novo_horario
            tarefa.save()

            return redirect('lista_tarefas_agendadas')
    else:
        form = EditarHorarioForm(instance=tarefa)

    return render(request, 'index/editar/editar_horario_tarefa.html', {'form': form, 'tarefa': tarefa})

def enviar_whatsapp(request, laudos_paciente_id):
    laudo = get_object_or_404(Laudo, id=laudos_paciente_id)
    # Seção crítica
    
    # Configurar o fuso horário padrão
    utc_minus3 = timezone.get_default_timezone()

    # Obter a hora atual no fuso horário padrão
    now_utc_minus3 = timezone.now().astimezone(utc_minus3)

    # Criar a hora_agendada respeitando o fuso horário padrão
    #hora_agendada = now_utc_minus3.replace(hour=20, minute=0, second=0, microsecond=0)
    hora_agendada = laudo.hora_envio
    # Verificar se já passou da hora agendada
    # Verificar se já passou da hora agendada
    if now_utc_minus3.replace(tzinfo=None) > hora_agendada.replace(tzinfo=None):
        # Se sim, agendar para amanhã às 20h
        hora_agendada += timedelta(days=1)

    novo_horario = hora_agendada
    while Schedule.objects.filter(next_run=novo_horario):
    # Se sim, adicione 1 minuto ao novo horário
        novo_horario += timezone.timedelta(minutes=5)

    try:
        # Agendar a primeira tarefa
        task = schedule(
            'apps.index.tasks.enviar_whatsapp_task',
            laudo.id,
            name=f'Whatsapp - {laudo.tutor} - {laudo.paciente} - {laudo.tipo_laudo}',
            schedule_type='O',
            next_run=novo_horario,
        )
        
        

        
        messages.success(request, "Tarefa agendada com sucesso")

        # Redirecione para a página de edição de horário com o ID da tarefa
        return redirect('lista_tarefas_agendadas')
    except Exception as e:
        messages.error(request, f"Erro ao agendar tarefa: {str(e)}")
        return redirect('exibicao', paciente_id=laudo.paciente.id)
    

from decimal import Decimal
from django.db.models import Sum

def laudos_hoje(request):
    data_selecionada = request.GET.get('data')

    print("Data recebida do formulário:", data_selecionada)

    if data_selecionada:
        # Converter a string da data em um objeto datetime
        data = datetime.strptime(data_selecionada, '%Y-%m-%d').date()

        print("Data convertida para datetime:", data)

        # Filtra os laudos criados na data selecionada
        laudos_hoje = Laudo.objects.filter(data__date=data).order_by('-data')
    else:
        # Se nenhuma data foi selecionada, filtra os laudos criados hoje
        laudos_hoje = Laudo.objects.filter(data__date=datetime.now().date()).order_by('-data')
        

    total_preco = laudos_hoje.aggregate(Sum('preco'))['preco__sum'] or Decimal('0.00')

    print("Número de laudos encontrados:", laudos_hoje.count())

    context = {'laudos': laudos_hoje, 'total_preco': total_preco}
    return render(request, 'laudos_hoje.html', context)

def atualizar_entrega_whats_laudo(request, laudo_paciente_id):
    laudo = Laudo.objects.get(pk=laudo_paciente_id)
    laudo.entregue_whats = not laudo.entregue_whats
    laudo.save()
    return redirect('laudos_hoje')

def atualizar_entrega_email_laudo(request, laudo_paciente_id):
    laudo = Laudo.objects.get(pk=laudo_paciente_id)
    laudo.entregue_email = not laudo.entregue_email
    laudo.save()
    return redirect('laudos_hoje')

def atualizar_laudo_pronto(request, laudo_paciente_id):
    laudo = Laudo.objects.get(pk=laudo_paciente_id)
    laudo.laudo_pronto = not laudo.laudo_pronto
    laudo.save()
    return redirect('laudos_hoje')



def editar_precos_laudo_hoje(request):
    # Obtenha a data de hoje
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Filtra os laudos criados hoje
    laudos_hoje = Laudo.objects.filter(data__gte=hoje).order_by('-data')

    context = {'laudos': laudos_hoje}
    return render(request, 'editar_precos_laudo_hoje.html', context)

def atualizar_preco_laudo(request, laudo_id):
    laudo = get_object_or_404(Laudo, id=laudo_id)

    if request.method == 'POST':
        novo_preco = request.POST.get('novo_preco')
        # Faça o processamento necessário para salvar o novo preço no objeto Laudo
        laudo.preco = novo_preco
        laudo.save()

        return JsonResponse({'mensagem': 'Preço atualizado com sucesso!'})

    return render(request, 'atualizar_preco_laudo.html', {'laudo': laudo})

import locale

def salvar_todos_precos_laudo(request):
    if request.method == 'POST':
        # Configura a localização para o Brasil
        locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')

        for laudo_id, novo_preco in request.POST.items():
            if laudo_id.startswith('laudo_'):
                laudo_id = laudo_id.replace('laudo_', '')
                laudo = Laudo.objects.get(id=laudo_id)

                # Converte o preço para o formato esperado pelo Django
                novo_preco = locale.atof(novo_preco)
                
                laudo.preco = novo_preco
                laudo.save()

        return redirect('editar_precos_laudo_hoje')

    return render(request, 'editar_precos_laudo_hoje.html')

from django.urls import reverse


def editar_preco_laudo(request, laudo_id):
    laudo = get_object_or_404(Laudo, id=laudo_id)

    if request.method == 'POST':
        novo_preco = request.POST.get('novo_preco')
        # Salve o novo preço no laudo
        laudo.preco = novo_preco
        laudo.save()
        # Redirecione para a página de listagem de laudos com os filtros preservados
        return redirect(reverse('laudo_list') + f'?{request.GET.urlencode()}')

    context = {'laudo': laudo}
    return render(request, 'editar_preco_laudo.html', context)

def deletar_laudo_ajax(request, laudo_id):
    laudo = Laudo.objects.get(pk=laudo_id)
    laudo.delete()
    return JsonResponse({'mensagem': 'Laudo excluído com sucesso'})

def editar_pdf(request, laudos_paciente_id):
    try:
        # Obtenha o objeto do banco de dados
        laudo = Laudo.objects.get(id=laudos_paciente_id)

            # Configurando o link para AWS
        data_atual = laudo.data.strftime("%Y-%m-%d")
        aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
        s3_filename_format = s3_filename.replace(" ", "+")
        pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

        # Crie o QR code com o link para AWS
        qr_img = qrcode.make(pdf_link)
        
        # Converta o QR code em BytesIO
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        
        # Converta o BytesIO em imagem PIL
        qr_pil_img = Image.open(qr_bytes)
        
        # Converta a imagem do QR code em base64
        qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode()
        
        # Adicione a imagem codificada ao contexto
        context = {'laudo': laudo, 'qr_base64': qr_base64}
        
        # Renderize o template com o contexto
        html_index = render_to_string('export-pdf.html', context)

        # Crie uma instância do HTML usando weasyprint
        weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')

        # Gere o PDF
        pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])

       # Configurar as credenciais do AWS
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        # Configurar o cliente S3
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        data_atual = laudo.data.strftime("%Y-%m-%d")
        # Nome do arquivo no S3
        s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
        s3_filename_format = s3_filename.replace(" ", "+")
        # Criar um objeto de bytes em memória
        pdf_bytes_io = io.BytesIO(pdf)

        # Fazer upload do PDF para o S3
        s3.upload_fileobj(pdf_bytes_io, aws_storage_bucket_name, s3_filename)

        # Fechar o objeto de bytes em memória (opcional)
        pdf_bytes_io.close()

        # Faça as edições necessárias no PDF (implemente esta parte conforme suas necessidades)

        messages.success(request, "PDF editado com sucesso")

    except Laudo.DoesNotExist:
        messages.error(request, "Laudo não encontrado")
    except Exception as e:
        messages.error(request, f"Erro ao editar PDF: {str(e)}")

    return redirect('exibicao', paciente_id=laudo.paciente.id)

def salvar_laudo_aws(request, laudos_paciente_id):
    laudo = get_object_or_404(Laudo, id=laudos_paciente_id)
    try:
        # Agendar a segunda tarefa
        task = schedule(
            'apps.index.tasks.salvar_laudo_aws_task',
            laudo.id,
            name=f'Salvando no aws - {laudo.paciente} - {laudo.tipo_laudo}',
            schedule_type='O',
            next_run=datetime.now() + timedelta(seconds=5),  # Agendar para 5 segundos a partir de agora
        )
    except Exception as e:
        messages.error(request, f"Erro ao agendar tarefa: {str(e)}")
        return redirect('exibicao', paciente_id=laudo.paciente.id)

def enviar_laudo(request, laudos_paciente_id):
    laudo = get_object_or_404(Laudo, id=laudos_paciente_id)

    

    #enviar_whatsapp(request, laudos_paciente_id=laudo.id)
    enviar_pdf(request, laudos_paciente_id=laudo.id)  # Passa a instância do modelo diretamente
    salvar_laudo_aws(request, laudos_paciente_id=laudo.id) 

    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    
    
    data_atual = laudo.data.strftime("%Y-%m-%d")
    
    # Nome do arquivo no S3
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    s3_filename_format = s3_filename.replace(" ", "+")
    

    # Gerar o link para o PDF no S3
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

    # Inicializar a variável mensagem_vet com um valor padrão
    mensagem_vet = ""

    # Montar a parte da mensagem relacionada ao veterinário
    if laudo.veterinario:
        mensagem_vet += f"Veterinário - {laudo.veterinario} - {laudo.veterinario.telefone}"
    
    if laudo.clinica:
        mensagem_vet += f" \n\n Clínica - {laudo.clinica} - {laudo.clinica.telefone}"
        
    if laudo.tutor:
        mensagem_vet += f" \n\n Tutor -  {laudo.tutor} - {laudo.tutor.telefone}"  
   
    mensagem = f"{mensagem_vet}\n\n {laudo.paciente} - {laudo.tipo_laudo}  \n\n Mensagem: \n\n*LAUDO DISPONÍVEL!*\n\nSegue abaixo o link para acessar o laudo de *{laudo.tipo_laudo}* do(a) paciente *{laudo.paciente}* - tutor *{laudo.tutor}*\n\n{pdf_link}\n\n*Caso o link não apareça clicável, salve este número em sua lista de contatos, para liberar o link.*\n\nAtenciosamente, *Dra. Jéssica Yasminne Diagnostico Veterinário*"

    # Substituir quebras de linha por <br> para exibição no HTML
    mensagem_html = mensagem.replace('\n', '<br>')
    
    # Atualiza o campo mensagem_whatsapp no objeto Laudo
    laudo.mensagem_whatsapp = mensagem_html
    laudo.enviar_agora = True
    laudo.save()

    # Redirecione para a página de edição de horário com o ID da tarefa
    return redirect('lista_tarefas_agendadas')

def excluir_pdf_aws(request,laudo):
    try:
        # Configurar as credenciais do AWS
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        # Criar um cliente S3
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        data_atual = laudo.data.strftime("%Y-%m-%d")
        # Nome do arquivo no S3
        s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'

        # Excluir o objeto PDF no S3
        s3.delete_object(Bucket=aws_storage_bucket_name, Key=s3_filename)

        messages.success(request, f'PDF {s3_filename} excluído com sucesso.')
    except NoCredentialsError:
        messages.error(request, 'Credenciais do AWS não configuradas corretamente ou ausentes.')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao excluir o PDF: {str(e)}')



def sua_funcao_para_excluir_pdf(request, laudos_paciente_id):
    try:
        # Obtenha o objeto do banco de dados
        laudo = Laudo.objects.get(id=laudos_paciente_id)

        # Exclua o PDF na AWS
        excluir_pdf_aws(request, laudo)

        # Faça outras ações conforme necessário

        messages.success(request, "PDF excluído com sucesso")

    except Laudo.DoesNotExist:
        messages.error(request, "Laudo não encontrado")
    except Exception as e:
        messages.error(request, f"Erro ao excluir PDF: {str(e)}")

    return redirect('exibicao', paciente_id=laudo.paciente.id)
    

def baixar_diretorio_s3(request, diretorio_s3):
    try:
        # Decodificar o diretório S3
        diretorio_s3_decodificado = unquote(diretorio_s3)

        # Configurar as credenciais do AWS
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        # Criar um cliente S3
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Obter uma lista de objetos no diretório S3
        response = s3.list_objects_v2(Bucket=aws_storage_bucket_name, Prefix=diretorio_s3_decodificado)
        objetos_s3 = response.get('Contents', [])

        # Criar um arquivo zip em memória
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for objeto in objetos_s3:
                # Obter o nome do arquivo no S3
                s3_filename = objeto['Key']
                # Obter o conteúdo do arquivo no S3
                file_content = s3.get_object(Bucket=aws_storage_bucket_name, Key=s3_filename)['Body'].read()

                # Adicionar o arquivo ao zip com o mesmo nome
                zip_file.writestr(s3_filename, file_content)

        # Criar a resposta HTTP com o conteúdo do arquivo zip
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        # Definir o nome do arquivo zip para download
        response['Content-Disposition'] = f'attachment; filename={diretorio_s3_decodificado.split("_", 1)[-1]}.zip'

        return response

    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao baixar o diretório {diretorio_s3_decodificado} no S3: {str(e)}')
        return render(request, 'listar_diretorios.html', {'erro': str(e)})
    
def listar_diretorios_s3(request):
    try:
        # Configurar as credenciais do AWS
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        # Criar um cliente S3
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Especificar o diretório S3 que você deseja listar
        diretorio_s3 = 'laudos/'

        # Listar diretórios no S3
        response = s3.list_objects_v2(Bucket=aws_storage_bucket_name, Prefix=diretorio_s3, Delimiter='/')
        diretorios = [common_prefix['Prefix'].rstrip('/') for common_prefix in response.get('CommonPrefixes', [])]

        # Obter datas únicas disponíveis no formato YYYY-MM
        datas_disponiveis = list(set([diretorio.split('/')[1][:7] for diretorio in diretorios]))

        print("Diretórios antes do filtro:", diretorios)

        # Se houver um parâmetro de filtro de data na URL, aplique o filtro
        filtro_data = request.GET.get('filtro_data', 'todos')
        print("Filtro de data:", filtro_data)

        if filtro_data != 'todos':
            diretorios_filtrados = [diretorio for diretorio in diretorios if diretorio.startswith(f'laudos/{filtro_data}')]
        else:
            diretorios_filtrados = diretorios

        print("Diretórios após o filtro:", diretorios_filtrados)

        return render(request, 'listar_diretorios.html', {'diretorios': diretorios_filtrados, 'datas_disponiveis': datas_disponiveis, 'filtro_data': filtro_data})

    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao listar os diretórios no S3: {str(e)}')
        return render(request, 'listar_diretorios.html', {'erro': str(e)})


def laudo_list(request):
    # Lógica para filtrar os laudos com base nos parâmetros da URL
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_laudo = request.GET.get('tipo_laudo')
    clinica = request.GET.get('clinica')

    laudos = Laudo.objects.all()

    if data_inicio and data_fim:
        laudos = laudos.filter(data__range=[data_inicio, data_fim])

    if tipo_laudo:
        laudos = laudos.filter(tipo_laudo=tipo_laudo)

    if clinica:
        laudos = laudos.filter(clinica=clinica)

    # Ordenar pela data (da mais antiga para a mais recente)
    laudos = laudos.order_by('data')

    # Obtendo a lista de tipos de laudo e clínicas para o formulário de filtro
    laudos_tipos = LaudosPadrao.objects.all()
    clinicas = Clinica.objects.all()

    # Convertendo feriados para uma lista de strings no formato 'YYYY-MM-DD'
    feriados = [feriado.strftime('%Y-%m-%d') for feriado in feriados]

    context = {
        'laudos': laudos,
        'laudos_tipos': laudos_tipos,
        'clinicas': clinicas,
        'tipo_laudo_selecionado': tipo_laudo,
        'feriados': feriados,  # Adicione os feriados ao contexto
    }

    return render(request, 'laudo_list.html', context)



def relatorio_exames(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    clinica = request.GET.get('clinica')

    laudos_filtrados = Laudo.objects.all()

    if data_inicio and data_fim:
        laudos_filtrados = laudos_filtrados.filter(data__range=[data_inicio, data_fim])

    if clinica:
        laudos_filtrados = laudos_filtrados.filter(clinica__id=clinica)

    # Calcula a contagem de exames por tipo
    contagem_exames = laudos_filtrados.values('tipo_laudo__nome_exame').annotate(
        contagem=Count('tipo_laudo__nome_exame'),
        valor_total=Sum('preco')  # Adiciona a soma dos preços como 'valor_total'
    )

    # Calcula a contagem de exames por clínica
    contagem_clinicas = laudos_filtrados.values('clinica__nome').annotate(
        contagem=Count('id'),
        valor_total=Sum('preco')
    )

    # Converte o resultado em um dicionário para facilitar o acesso no template
    contagem_exames = {item['tipo_laudo__nome_exame']: item for item in contagem_exames}
    
   # Converte o resultado em um dicionário para facilitar o acesso no template
    contagem_clinicas = {item['clinica__nome']: {'contagem': item['contagem'], 'valor_total': item['valor_total']} for item in contagem_clinicas}

    # Calcula o total de exames e o valor total
    total_exames = sum(item['contagem'] for item in contagem_exames.values())
    total_valor = sum(item['valor_total'] for item in contagem_exames.values() if item['valor_total'])
    ticket_medio = total_valor / total_exames
    laudos_padrao = LaudosPadrao.objects.all()

    # Obtendo a lista de clínicas para o formulário de filtro
    clinicas = Clinica.objects.all()

    total_exames_data = {
        'labels': [clinic.nome for clinic in clinicas],
        'values': [contagem_clinicas.get(clinic.nome, {'contagem': 0}).get('contagem', 0) for clinic in clinicas],
    }

    valor_total_data = {
        'labels': [clinic.nome for clinic in clinicas],
        'values': [float(contagem_clinicas.get(clinic.nome, {'valor_total': 0}).get('valor_total', 0)) for clinic in clinicas],
    }

    context = {
        'clinicas': clinicas,
        'contagem_exames': contagem_exames,
        'total_exames': total_exames,
        'total_valor': total_valor,
        'laudos_padrao': laudos_padrao,
        'contagem_clinicas': contagem_clinicas,
        'total_exames_data': total_exames_data,
        'valor_total_data': valor_total_data,
        'ticket_medio' : ticket_medio,
    }

    return render(request, 'relatorio_exames.html', context)

from django.db import models
from django.utils import timezone
import pandas as pd
from workalendar.america import Brazil
import calendar
from workalendar.america import Brazil
import holidays

def calcular_relatorio(request):
    # Obtendo informações sobre dias úteis e feriados
    hoje = datetime.now()
    primeiro_dia_mes = hoje.replace(day=1)
    ultimo_dia_mes = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])

    dias_uteis = []
    feriados = []

    # Iterar sobre cada dia no mês
    current_day = primeiro_dia_mes
    while current_day <= ultimo_dia_mes:
        # Verificar se o dia é útil (não é sábado ou domingo)
        if current_day.weekday() < 5:
            dias_uteis.append(current_day.date())
        else:
            # Se for sábado ou domingo, apenas ignore, não adicionando a nenhum lista
            pass

        current_day += timedelta(days=1)

    # Obter feriados nacionais do Brasil
    cal_br = Brazil()
    feriados_nacionais = [data for data, nome in cal_br.holidays(hoje.year)]

    # Obter feriados municipais de Recife
    feriados_recife = holidays.BR(state='PE', years=[hoje.year])

    # Atualizar a lista de feriados com os feriados nacionais e municipais
    feriados += feriados_nacionais + list(feriados_recife)

    total_dias_uteis = len(dias_uteis)
    total_feriados = len(feriados)

    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            mes_ano = form.cleaned_data['mes']
            # Separar o mês e o ano
            mes, ano = mes_ano.split('/')
            dias_trabalhados_total = form.cleaned_data['dias_trabalhados_total']

            # Obter a lista de laudos para o mês e ano escolhidos
            laudos_do_mes = Laudo.objects.filter(data__month=mes, data__year=ano)

            # Contando o número de dias únicos
            dias_trabalhados_basico = laudos_do_mes.values('data__day').distinct().count()
            dias_sem_exame = form.cleaned_data['dias_sem_exame']
            dias_trabalhados_realizados = dias_trabalhados_basico + dias_sem_exame

            # Somatório dos preços de todos os laudos
            somatorio_precos = laudos_do_mes.aggregate(soma_precos=models.Sum('preco'))['soma_precos'] or 0

            # Média de preço por dia
            media_preco_por_dia = somatorio_precos / dias_trabalhados_realizados if dias_trabalhados_realizados > 0 else 0

            # Média multiplicada pelo total de dias escolhidos
            resultado_final = media_preco_por_dia * dias_trabalhados_total
            
            # Consulta para obter os laudos do dia atual
            hoje = timezone.now()
            laudos_do_dia = Laudo.objects.filter(data__date=hoje.date())
            faturamento_do_dia = laudos_do_dia.aggregate(soma_precos=models.Sum('preco'))['soma_precos'] or 0
            
            return render(request, 'relatorio/resultado.html', {
                'dias_trabalhados_realizados': dias_trabalhados_realizados,
                'somatorio_precos': somatorio_precos,
                'media_preco_por_dia': media_preco_por_dia,
                'resultado_final': resultado_final,
                'faturamento_dia_atual': faturamento_do_dia,
                
            })
    else:
        form = RelatorioForm()
        
        return render(request, 'relatorio/calcular_relatorio.html', {
            'form': form,
            'dias_uteis': dias_uteis,
            'feriados': feriados,
            'total_dias_uteis': total_dias_uteis,
            'total_feriados': total_feriados,
        })
    

def editar_observacao_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        nova_observacao = request.POST.get('nova_observacao')
        paciente.observacao = nova_observacao
        paciente.save()
        # Redirecionar para a página de detalhes do paciente após a edição
        return redirect('exibicao', paciente.id)

    return render(request, 'editar_observacao_paciente.html', {'paciente': paciente})

from django.forms.models import model_to_dict

def editar_inventario(request):
    # Obtém a instância única do modelo Inventario, ou cria uma nova se não existir
    inv_instance, _ = Inventario.objects.get_or_create()

    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        try:
            # Atualiza os valores do inventário com base nos dados do formulário
            inv_instance.alcool = float(request.POST.get('alcool', '0.0').replace(',', '.'))
            inv_instance.gel_usg = float(request.POST.get('gel_usg', '0.0').replace(',', '.'))
            inv_instance.seringa_10ml = float(request.POST.get('seringa_10ml', '0.0').replace(',', '.'))
            inv_instance.seringa_5ml = float(request.POST.get('seringa_5ml', '0.0').replace(',', '.'))
            inv_instance.seringa_3ml = float(request.POST.get('seringa_3ml', '0.0').replace(',', '.'))
            inv_instance.agulha_azul = float(request.POST.get('agulha_azul', '0.0').replace(',', '.'))
            inv_instance.cateter_azul = float(request.POST.get('cateter_azul', '0.0').replace(',', '.'))
            inv_instance.cateter_rosa = float(request.POST.get('cateter_rosa', '0.0').replace(',', '.'))
            inv_instance.gaze_n_esteril = float(request.POST.get('gaze_n_esteril', '0.0').replace(',', '.'))
            inv_instance.pano_de_campo = float(request.POST.get('pano_de_campo', '0.0').replace(',', '.'))
            inv_instance.essencia_spray = float(request.POST.get('essencia_spray', '0.0').replace(',', '.'))
            inv_instance.papel_quadrado = float(request.POST.get('papel_quadrado', '0.0').replace(',', '.'))
            inv_instance.desinfetante_herbal = float(request.POST.get('desinfetante_herbal', '0.0').replace(',', '.'))
            inv_instance.prope = float(request.POST.get('prope', '0.0').replace(',', '.'))
            inv_instance.seringa_60ml = float(request.POST.get('seringa_60ml', '0.0').replace(',', '.'))
            inv_instance.scal_azul = float(request.POST.get('scal_azul', '0.0').replace(',', '.'))
            # Repita para os outros campos do inventário

            # Salva as alterações
            inv_instance.save()
        except ValueError:
            # Se ocorrer um erro de conversão para float, exibe uma mensagem de erro
            error_message = "Todos os valores devem ser números decimais."
            return render(request, 'index/editar_inventario.html', {'inventario': inv_instance, 'error_message': error_message})

    # Renderiza o template com os valores atuais do inventário
    return render(request, 'index/editar_inventario.html', {'inventario': inv_instance})

def filtrar_laudos(request):
    if request.method == 'GET':
        mes = request.GET.get('mes')
        if mes:
            mes = int(mes)
        else:
            mes = datetime.now().month

        ano = request.GET.get('ano')
        if ano:
            ano = int(ano)
        else:
            ano = datetime.now().year
            
        forma_pagamento_filtro = request.GET.get('forma_pagamento')
        data_pagamento_filtro = request.GET.get('data_pagamento')
        clinica_filtro = request.GET.get('clinica')  # Novo campo para filtrar por clínica
        

        laudos = Laudo.objects.filter(data__month=mes, data__year=ano).order_by('-data')

        # Verifica se a opção de filtro para forma_pagamento foi selecionada
        if forma_pagamento_filtro:
            try:
                forma_pagamento_filtro = int(forma_pagamento_filtro)
                laudos = laudos.filter(forma_pagamento_id=forma_pagamento_filtro)
            except ValueError:
                # Se a conversão para int falhar, simplesmente não aplique o filtro
                pass

        # Verifica se a opção de filtro para data_pagamento é diferente de "ambos"
        if data_pagamento_filtro != 'ambos':
            if data_pagamento_filtro == 'null':
                laudos = laudos.filter(data_pagamento__isnull=True)
            elif data_pagamento_filtro == 'not_null':
                laudos = laudos.exclude(data_pagamento__isnull=True)

        # Verifica se foi enviado um filtro para laudo.clinica e aplica-o à consulta
        if clinica_filtro:
            laudos = laudos.filter(clinica_id=clinica_filtro)

        
        # Calcula o somatório de todos os valores de laudo.preco
        total_precos = laudos.aggregate(Sum('preco'))['preco__sum']
        total_precos_real = laudos.aggregate(Sum('preco_real'))['preco_real__sum']
        # Calcula o somatório de preços para cada clínica presente nos laudos
        somatorio_por_clinica = {}
        for laudo in laudos:
            clinica_nome = laudo.clinica
            if clinica_nome not in somatorio_por_clinica:
                somatorio_por_clinica[clinica_nome] = 0
            somatorio_por_clinica[clinica_nome] += laudo.preco

        formas_pagamento = FormaDePagamento.objects.all()
        clinicas = Clinica.objects.all()  # Carrega todas as clínicas para o campo de seleção

        # Ordena o dicionário somatorio_por_clinica com base nos valores (somatório de preços)
        somatorio_por_clinica_ordenado = dict(sorted(somatorio_por_clinica.items(), key=lambda item: item[1], reverse=True))
        return render(request, 'controle_financeiro.html', {'laudos': laudos, 'formas_pagamento': formas_pagamento, 'total_precos': total_precos,'total_precos_real':total_precos_real ,'somatorio_por_clinica': somatorio_por_clinica_ordenado, 'clinicas': clinicas})

    
    laudos = Laudo.objects.all()
    context = {'laudos': laudos}
    return render(request, 'filtrar_laudos.html', context)


from django.http import HttpResponseRedirect



def salvar_alteracao_controle(request):
    if request.method == 'POST':
        laudos_ids = request.POST.getlist('laudo_ids')
        # Recupere os parâmetros dos filtros do objeto request
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        forma_pagamento_filtro = request.POST.get('forma_pagamento')
        data_pagamento_filtro = request.POST.get('data_pagamento')
        clinica_filtro = request.POST.get('clinica')
                
        for laudo_id in laudos_ids:
            preco = request.POST.get(f'preco_{laudo_id}', '') 
            preco_real = request.POST.get(f'preco_real_{laudo_id}', '')  
            data_pagamento = request.POST.get(f'data_pagamento_{laudo_id}', '')  
            nota_fiscal = request.POST.get(f'nota_fiscal_{laudo_id}')
            forma_pagamento_id = request.POST.get(f'forma_pagamento_{laudo_id}', '') 
            observacao_pagamento = request.POST.get(f'observacao_pagamento_{laudo_id}', '') 

            preco = preco.replace(',', '.') if preco else None
            preco_real = preco_real.replace(',', '.') if preco_real else None  
            data_pagamento = data_pagamento.replace(',', '.') if data_pagamento else None  
            observacao_pagamento = observacao_pagamento.replace(',', '.') if observacao_pagamento else None

            laudo = Laudo.objects.get(id=laudo_id)
            laudo.preco = preco
            laudo.preco_real = preco_real
            laudo.data_pagamento = data_pagamento
            laudo.observacao_pagamento = observacao_pagamento
            laudo.nota_fiscal = True if nota_fiscal else False
            
            if forma_pagamento_id:  # Verifica se a forma de pagamento foi selecionada
                forma_pagamento = FormaDePagamento.objects.get(pk=forma_pagamento_id)
                laudo.forma_pagamento = forma_pagamento  # Associa a forma de pagamento ao laudo
            
            laudo.save()
        
        messages.success(request, 'Alterações salvas com sucesso!')
        
        # Redirecionamento de volta para a página de filtragem com os parâmetros de filtro
        url = reverse('filtrar_laudos')
        url += f'?mes={mes}&ano={ano}&forma_pagamento={forma_pagamento_filtro}&data_pagamento={data_pagamento_filtro}&clinica={clinica_filtro}'
        
        return HttpResponseRedirect(url)
    
    # Se não for um POST, retorne à página de filtragem sem fazer alterações
    return HttpResponseRedirect(reverse('filtrar_laudos'))


