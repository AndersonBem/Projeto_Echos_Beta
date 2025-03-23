# apps/index/context_processors.py

from datetime import date, timedelta
from .models import Acompanhamento  # Supondo que o modelo esteja no app "index"

def acompanhamento_7_dias(request):
    hoje = date.today()
    sete_dias_depois = hoje + timedelta(days=7)
    
    # Verifica se há acompanhamentos para essa data
    acompanhamento_futuro =  Acompanhamento.objects.filter(data__range=[hoje, sete_dias_depois]).exists()
    
    return {'acompanhamento_7_dias': acompanhamento_futuro}