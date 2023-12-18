from django.shortcuts import render,redirect, get_object_or_404
from apps.index.models import Veterinario, Clinica, Paciente, Tutor, LaudosPadrao, Frases, Laudo, LaudoImagem
from django.contrib import messages
from apps.index.forms import VeterinarioForms, ClinicaForms, PacienteForms, TutorForms, PacienteCaninoForms, LaudoForms, RacaFelinoForms, RacaCaninoForms, LaudoPadraoForms, FrasesForm,\
NovaImagemForm
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
            return redirect(reverse('exibicao', kwargs={'paciente_id': paciente_id}))
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


def deletar_imagem(request, imagem_id):
    imagem = get_object_or_404(LaudoImagem, id=imagem_id)
    laudo_id = imagem.laudo.id  # Captura o ID do laudo antes de deletar a imagem
    imagem.delete()
    return redirect('exibir_laudo', laudos_paciente_id=laudo_id)


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
            return redirect(reverse('exibir_laudo', kwargs={'laudos_paciente_id': laudo_id}))
    else:
        form = NovaImagemForm()

    return render(request, 'index/adicionar_imagem.html', {'form': form, 'laudo': laudo})





def export_pdf(request, laudos_paciente_id): 
    laudo = Laudo.objects.get(id=laudos_paciente_id)
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})  
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



def exibir_pdf(request, laudos_paciente_id):
    laudo = Laudo.objects.get(id=laudos_paciente_id)
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})  
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
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])

    # Enviar o e-mail
    subject = f'Laudo de {laudo.paciente}'
    message_body = f'Prezado(a) Senhor(a) {laudo.tutor}, \n\nSegue em anexo o laudo do exame de {laudo.paciente}, \n\nAtenciosamente, Dra. Jéssica Yasminne Diagnóstico por Imagem Veterinário '  # Modifique conforme necessário
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [laudo.email]

    email = EmailMessage(subject, message_body, from_email, to_email)
    email.content_subtype = ''
    email.attach(f'Laudo - {laudo.paciente} - {laudo.data}.pdf', pdf, 'application/pdf')
    # email.send()  # Remova ou mantenha dependendo se deseja enviar o email imediatamente ou não

    # Configurar o fuso horário padrão
    utc_minus3 = timezone.get_default_timezone()

    # Obter a hora atual no fuso horário padrão
    now_utc_minus3 = timezone.now().astimezone(utc_minus3)

    # Criar a hora_agendada respeitando o fuso horário padrão
    #hora_agendada = now_utc_minus3.replace(hour=20, minute=00, second=0, microsecond=0)
    hora_agendada = laudo.hora_envio
    # Verificar se já passou da hora agendada
    if now_utc_minus3 > hora_agendada:
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
            name=f'Email para {laudo.tutor}, tutor de : {laudo.paciente} - Exame : {laudo.tipo_laudo}',
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
    
    # Configurar o fuso horário padrão
    utc_minus3 = timezone.get_default_timezone()

    # Obter a hora atual no fuso horário padrão
    now_utc_minus3 = timezone.now().astimezone(utc_minus3)

    # Criar a hora_agendada respeitando o fuso horário padrão
    #hora_agendada = now_utc_minus3.replace(hour=20, minute=0, second=0, microsecond=0)
    hora_agendada = laudo.hora_envio
    # Verificar se já passou da hora agendada
    if now_utc_minus3 > hora_agendada:
        # Se sim, agendar para amanhã às 20h
        hora_agendada += timedelta(days=1)

    novo_horario = hora_agendada
    while Schedule.objects.filter(next_run=novo_horario):
    # Se sim, adicione 1 minuto ao novo horário
        novo_horario += timezone.timedelta(minutes=5)

    try:
        task = schedule(
            'apps.index.tasks.enviar_whatsapp_task',
            laudo.id,
            name=f'Whatsapp para {laudo.tutor}, tutor de : {laudo.paciente} - Exame : {laudo.tipo_laudo}',
            schedule_type='O',
            next_run=novo_horario,
            
        )

        
        messages.success(request, "Tarefa agendada com sucesso")

        # Redirecione para a página de edição de horário com o ID da tarefa
        return redirect('lista_tarefas_agendadas')
    except Exception as e:
        messages.error(request, f"Erro ao agendar tarefa: {str(e)}")
        return redirect('exibicao', paciente_id=laudo.paciente.id)
    

def laudos_hoje(request):
    # Filtra os laudos criados hoje
    laudos_hoje = Laudo.objects.filter(data=datetime.now().date())

    context = {'laudos': laudos_hoje}
    return render(request, 'laudos_hoje.html', context)

def deletar_laudo_ajax(request, laudo_id):
    laudo = Laudo.objects.get(pk=laudo_id)
    laudo.delete()
    return JsonResponse({'mensagem': 'Laudo excluído com sucesso'})

def editar_pdf(request, laudos_paciente_id):
    try:
        # Obtenha o objeto do banco de dados
        laudo = Laudo.objects.get(id=laudos_paciente_id)

        # Renderize o template para HTML
        html_index = render_to_string('export-pdf.html', {'laudo': laudo})  

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

        # Nome do arquivo no S3
        s3_filename = f'laudos/{laudo.data}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
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

def enviar_laudo(request, laudos_paciente_id):
    laudo = get_object_or_404(Laudo, id=laudos_paciente_id)

    enviar_pdf(request, laudos_paciente_id=laudo.id)  # Passa a instância do modelo diretamente

    enviar_whatsapp(request, laudos_paciente_id=laudo.id)

    

    # Redirecione para a página de edição de horário com o ID da tarefa
    return redirect('lista_tarefas_agendadas')
    