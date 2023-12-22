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
import time
import asyncio

import pywhatkit

logger = logging.getLogger(__name__)


def enviar_pdf_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    # Seção crítica
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])

    lista_de_email = [
        laudo.tutor.email if laudo.tutor and laudo.tutor.email else None,                   # junior
        laudo.veterinario.email if laudo.veterinario and laudo.veterinario.email else None, # alexia
        laudo.clinica.email if laudo.clinica and laudo.clinica.email else None,             # katia
        laudo.email if laudo.email else None,                                              # Jessica
        laudo.email_extra if laudo.email_extra else None
    ]
    

    # Criar uma lista para armazenar os e-mails válidos
    emails_validos = [email for email in lista_de_email if email]
    
    mensagem = f'Prezado(a)\n\nSegue em anexo o laudo do exame de {laudo.paciente} , do tutor {laudo.tutor}, \n\nAtenciosamente, Dra. Jéssica Yasminne Diagnóstico por Imagem Veterinário'

    # Enviar o e-mail apenas se houver e-mails válidos
    if emails_validos:
        subject = f'Laudo de {laudo.tipo_laudo} do paciente {laudo.paciente}'
        message_body = mensagem
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = emails_validos
        data_laudo = laudo.data.strftime("%d/%m/%Y") 
        email = EmailMessage(subject,message_body,from_email,to_email)
        # Adição para verificar o corpo da mensagem
        
        print(message_body)
        print(emails_validos)
        email.content_subtype = ''
        email.attach(f'Laudo - {laudo.paciente} - {data_laudo}.pdf', pdf, 'application/pdf')
         # Adição para verificar o conteúdo do anexo
        

        # Adição para verificar a construção da mensagem completa
        
        email.send()
       


async def enviar_whatsapp_async(telefone, mensagem):
    telefone = re.sub(r'\D', '', str(telefone))
    if not telefone.startswith('55'):
        telefone = '+55' + telefone
    print(telefone)
    time.sleep(30)
    pywhatkit.sendwhatmsg(telefone, mensagem, datetime.now().hour, datetime.now().minute + 1, 15, True, 5)

    
def enviar_whatsapp_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    
    # Seção crítica
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 30px; } body { margin: 0; } img {width: 100%; }')])

    # Configurar as credenciais do AWS
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

    # Configurar o cliente S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    # Nome do arquivo no S3
    s3_filename = f'laudos/{data_atual}/{laudo.paciente}/paciente-{laudo.paciente}-Tutor-{laudo.tutor}-{laudo.tipo_laudo}.pdf'
    s3_filename_format = s3_filename.replace(" ", "+")
    # Criar um objeto de bytes em memória
    pdf_bytes_io = io.BytesIO(pdf)

    # Fazer upload do PDF para o S3
    s3.upload_fileobj(pdf_bytes_io, aws_storage_bucket_name, s3_filename)

    # Fechar o objeto de bytes em memória (opcional)
    pdf_bytes_io.close()

    # Gerar o link para o PDF no S3
    pdf_link = f'https://{aws_storage_bucket_name}.s3.amazonaws.com/{s3_filename_format}'

    # Montar a mensagem do WhatsApp com o link do PDF
    
   
    mensagem = f"*LAUDO PRONTO!*\n\nAbaixo encontra-se o link para acessar o laudo de *{laudo.tipo_laudo}* do(a) paciente *{laudo.paciente}* / tutor *{laudo.tutor}*\n\n{pdf_link}\n\n*Caso o link não apareça clicável, salve o número em sua lista de contatos, para liberar o link!*\n\nAtenciosamente, *Dra. Jéssica Yasminne Diagnostico Veterinário*"

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
        
