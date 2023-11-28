# tasks.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_q.tasks import async_task
from apps.index.models import Laudo
from django.conf import settings
import weasyprint
import traceback
import logging

logger = logging.getLogger(__name__)


def enviar_pdf_task(laudo_id):
    
    laudo = Laudo.objects.get(id=laudo_id)
    html_index = render_to_string('export-pdf.html', {'laudo': laudo})  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 0; } body { font-family: serif; margin: 20px; } img { width: 100%; }')])
        
    # Enviar o e-mail
    subject = f'Laudo de {laudo.paciente}'
    message_body = f'Prezado(a) Senhor(a) {laudo.tutor}, \n\nSegue em anexo o laudo do exame de {laudo.paciente}, \n\nAtenciosamente, Dra. Jéssica Yasminne Diagnóstico por Imagem Veterinário '  # Modifique conforme necessário
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [laudo.email]

    email = EmailMessage(subject, message_body, from_email, to_email)
    email.content_subtype = ''
    email.attach(f'Laudo - {laudo.paciente} - {laudo.data}.pdf', pdf, 'application/pdf')
    email.send()
    


