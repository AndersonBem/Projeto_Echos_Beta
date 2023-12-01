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
from datetime import datetime, timedelta
from django.utils import timezone  # Adicione esta linha para importar timezone
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def enviar_pdf_task(laudo_id):
    laudo = Laudo.objects.get(id=laudo_id)

    # Adquire a trava antes de executar a tarefa
    
    
    
    # Seção crítica
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 0; } body { font-family: serif; margin: 20px; } img { width: 100%; }')])

    # Enviar o e-mail
    subject = f'Laudo de {laudo.paciente}'
    message_body = f'Prezado(a) Senhor(a) {laudo.tutor}, \n\nSegue em anexo o laudo do exame de {laudo.paciente}, \n\nAtenciosamente, Dra. Jéssica Yasminne Diagnóstico por Imagem Veterinário '
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [laudo.email, laudo.email_extra, laudo.veterinario.email, laudo.clinica.email]
    data_laudo = laudo.data.strftime("%d/%m/%Y") 
    email = EmailMessage(subject, message_body, from_email, to_email)
    email.content_subtype = ''
    email.attach(f'Laudo - {laudo.paciente} - {data_laudo}.pdf', pdf, 'application/pdf')
    email.send()        
    
    
def enviar_whatsapp_task(laudo_id):
    pass
