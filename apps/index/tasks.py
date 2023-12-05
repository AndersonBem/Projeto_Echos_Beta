# tasks.py

from django_q.models import Schedule
from django.core.mail import EmailMessage
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

import asyncio

import pywhatkit

logger = logging.getLogger(__name__)


def enviar_pdf_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    # Seção crítica
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 0; } body { font-family: serif; margin: 20px; } img { width: 100%; }')])

    lista_de_email = [
        laudo.tutor.email if laudo.tutor and laudo.tutor.email else None,                   # junior
        laudo.veterinario.email if laudo.veterinario and laudo.veterinario.email else None, # alexia
        laudo.clinica.email if laudo.clinica and laudo.clinica.email else None,             # katia
        laudo.email if laudo.email else None                                              # Jessica
    ]

    # Criar uma lista para armazenar os e-mails válidos
    emails_validos = [email for email in lista_de_email if email]

    # Enviar o e-mail apenas se houver e-mails válidos
    if emails_validos:
        subject = f'Laudo de {laudo.paciente}'
        message_body = f'Prezado(a) Senhor(a) {laudo.tutor}, \n\nSegue em anexo o laudo do exame de {laudo.paciente}, \n\nAtenciosamente, Dra. Jéssica Yasminne Diagnóstico por Imagem Veterinário '
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = emails_validos
        data_laudo = laudo.data.strftime("%d/%m/%Y") 
        email = EmailMessage(subject, message_body, from_email, to_email)
        email.content_subtype = ''
        email.attach(f'Laudo - {laudo.paciente} - {data_laudo}.pdf', pdf, 'application/pdf')
        email.send()     


async def enviar_whatsapp_async(telefone, mensagem):
    telefone = re.sub(r'\D', '', str(telefone))
    if not telefone.startswith('55'):
        telefone = '+55' + telefone
    pywhatkit.sendwhatmsg(telefone, mensagem, datetime.now().hour, datetime.now().minute + 1, 7, True, 3)

    
def enviar_whatsapp_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    
    # Seção crítica
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 0; } body { font-family: serif; margin: 20px; } img { width: 100%; }')])

    # Configurar as credenciais do AWS
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    # Configurar o cliente S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Nome do arquivo no S3
    s3_filename = f'laudos/{laudo.data}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}.pdf'

    # Criar um objeto de bytes em memória
    pdf_bytes_io = io.BytesIO(pdf)

    # Fazer upload do PDF para o S3
    s3.upload_fileobj(pdf_bytes_io, aws_storage_bucket_name, s3_filename)

    # Fechar o objeto de bytes em memória (opcional)
    pdf_bytes_io.close()

    # Gerar o link para o PDF no S3
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename}'

    # Montar a mensagem do WhatsApp com o link do PDF
    mensagem = f"Olá! Aqui está o laudo do paciente: {pdf_link}"

    lista_de_telefones = [
        laudo.tutor.telefone if laudo.tutor else None,                   # empresa
        laudo.veterinario.telefone if laudo.veterinario else None,       # alexia
        laudo.clinica.telefone if laudo.clinica else None,               # katia
        laudo.telefone_extra if laudo.telefone_extra else None           # anderson
    ]

    # Criar uma lista para armazenar os números de telefone válidos
    telefones_validos = []
    agora = datetime.now()
    hora_atual = agora.hour
    minuto = datetime.now().minute+1

    # Adicionar números de telefone à lista apenas se não forem nulos ou vazios
    for telefone_original in lista_de_telefones:
        if telefone_original is not None and telefone_original != '':
            telefones_validos.append(telefone_original)

    # Enviar a mensagem no WhatsApp para números válidos
    
    # Criar uma lista para armazenar as tarefas assíncronas
    tasks = []

    # Iterar sobre os números de telefone válidos
    for telefone_original in telefones_validos:
        task = enviar_whatsapp_async(telefone_original, mensagem)
        tasks.append(task)

     # Criar e executar um evento de loop asyncio manualmente
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
        
