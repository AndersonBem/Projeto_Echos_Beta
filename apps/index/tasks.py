# tasks.py
from django.shortcuts import render,redirect, get_object_or_404
from django_q.models import Schedule
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_q.tasks import async_task
from apps.index.models import Laudo
from django.conf import settings
import weasyprint
import traceback
import logging
#agendamento whats
import re
from urllib.parse import quote
import webbrowser
import pyautogui
from time import sleep
import os
import io
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from django.utils import timezone  # Adicione esta linha para importar timezone
from django.db import IntegrityError
import pywhatkit as kt
import time
import asyncio
from django.utils.text import slugify
import qrcode
from PIL import Image
from io import BytesIO
import base64
import pywhatkit

logger = logging.getLogger(__name__)
from django.core.mail import EmailMessage

def enviar_pdf_task(laudo_id):
    # Obter o objeto de Laudo
    laudo = Laudo.objects.get(id=laudo_id)
    
    # Verificar se o Laudo existe
    if not laudo:
        return
    
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
    
    
    #mensagem = f"Abaixo encontra-se o link para acessar o laudo de {laudo.tipo_laudo} do(a) paciente {laudo.paciente} / tutor {laudo.tutor}\n\n{pdf_link}\n\nAtenciosamente, Dra. Jéssica Yasminne Diagnostico Veterinário"
    mensagem = f"LAUDO DISPONÍVEL!\n\nSegue abaixo o link para acessar o laudo de {laudo.tipo_laudo} do(a) paciente {laudo.paciente} - tutor {laudo.tutor}\n\n{pdf_link}\n\nAtenciosamente, Dra. Jéssica Yasminne Diagnostico Veterinário"
    # Configurar os detalhes do email
    subject = f'Laudo de {laudo.tipo_laudo} do paciente {laudo.paciente}'
    message_body = mensagem
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = []

    # Adicionar emails válidos à lista de destinatários
    if laudo.tutor and laudo.tutor.email:
        to_email.append(laudo.tutor.email)
    if laudo.veterinario and laudo.veterinario.email:
        to_email.append(laudo.veterinario.email)
    if laudo.clinica and laudo.clinica.email:
        to_email.append(laudo.clinica.email)
    if laudo.email_extra:
        to_email.append(laudo.email_extra)
    
    # Se não houver emails válidos, encerre a função
    if not to_email:
        return
    
    # Verificar se o email de destino está na lista de emails específicos
    if 'laribarbieri.vet@gmail.com' in to_email:
        # Criar o objeto de email com anexo
        email = EmailMessage(subject, message_body, from_email, to_email)
        email.attach(f'Laudo_{laudo.tipo_laudo}_{laudo.paciente}.pdf', pdf, 'application/pdf')
        email.send()
    else:
        # Criar o objeto de email sem anexo
        email = EmailMessage(subject, message_body, from_email, to_email)
        email.send()



async def enviar_whatsapp_async(nome, telefone, mensagem, telefones_validos):
    telefone = re.sub(r'\D', '', str(telefone))
    if not telefone.startswith('55'):
        telefone = '+55' + telefone
    print(f"Enviando para{telefones_validos}")
    print(f"Enviando para {nome} ({telefone})")
    
    time.sleep(15)
    pywhatkit.sendwhatmsg(telefone, mensagem, datetime.now().hour, datetime.now().minute + 1, 15, True, 10)
    time.sleep(15)

    
def enviar_whatsapp_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    
    
    data_atual = laudo.data.strftime("%Y-%m-%d")
    
    # Nome do arquivo no S3
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    s3_filename_format = s3_filename.replace(" ", "+")
    

    # Gerar o link para o PDF no S3
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

    # Montar a mensagem do WhatsApp com o link do PDF
    
   
    mensagem = f"*LAUDO DISPONÍVEL!*\n\nSegue abaixo o link para acessar o laudo de *{laudo.tipo_laudo}* do(a) paciente *{laudo.paciente}* - tutor *{laudo.tutor}*\n\n{pdf_link}\n\n*Caso o link não apareça clicável, salve este número em sua lista de contatos, para liberar o link.*\n\nAtenciosamente, *Dra. Jéssica Yasminne Diagnostico Veterinário*"

    

    lista_de_telefones = [
    laudo.tutor.telefone if laudo.tutor and laudo.tutor.telefone else None,                   # empresa
    laudo.veterinario.telefone if laudo.veterinario and laudo.veterinario.telefone else None, # alexia
    laudo.clinica.telefone if laudo.clinica and laudo.clinica.telefone else None,             # katia
    laudo.telefone_extra if laudo.telefone_extra else None                                       # anderson
]


    # Criar uma lista para armazenar os números de telefone válidos
    telefones_validos = []
    agora = datetime.now()
    

    # Adicionar números de telefone à lista apenas se não forem nulos ou vazios
    for telefone_original in lista_de_telefones:
        if telefone_original is not None and telefone_original != '':
            telefones_validos.append(telefone_original)

    # Enviar a mensagem no WhatsApp para números válidos
    
    # Criar uma lista para armazenar as tarefas assíncronas
    tasks = []

    # Mapear os nomes associados aos números de telefone
    nomes_telefones = {
        laudo.tutor.telefone if laudo.tutor else None: laudo.tutor.nome if laudo.tutor else None,
        laudo.veterinario.telefone if laudo.veterinario else None: laudo.veterinario.nome if laudo.veterinario else None,
        laudo.clinica.telefone if laudo.clinica else None: laudo.clinica.nome if laudo.clinica else None,
        laudo.telefone_extra if laudo.telefone_extra else None: None  # Insira o nome correspondente, se houver
    }

    # Iterar sobre os números de telefone válidos
    for telefone_original, nome_associado in nomes_telefones.items():
        if telefone_original is not None and telefone_original != '':
            task = enviar_whatsapp_async(nome_associado, telefone_original, mensagem, telefones_validos)
            tasks.append(task)

     # Criar e executar um evento de loop asyncio manualmente
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
        
def salvar_laudo_aws_task(laudo_id):
    laudo = get_object_or_404(Laudo, id=laudo_id)
    # Seção crítica


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

    # Configurar as credenciais do AWS
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    # Configurar o cliente S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    data_atual = laudo.data.strftime("%Y-%m-%d")
    
    # Nome do arquivo no S3
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    
    # Criar um objeto de bytes em memória
    pdf_bytes_io = io.BytesIO(pdf)

    # Fazer upload do PDF para o S3
    s3.upload_fileobj(pdf_bytes_io, aws_storage_bucket_name, s3_filename)

    # Fechar o objeto de bytes em memória (opcional)
    pdf_bytes_io.close()