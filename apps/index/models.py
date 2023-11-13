from django.db import models
from datetime import datetime, date
from django.utils import timezone
import os


# Create your models here.

def get_upload_path(instance, filename):
    # Obtém o nome do objeto
    nome_objeto = instance.nome
    # Obtém a extensão do arquivo
    extensao = filename.split('.')[-1]
    # Obtém a data atual
    data_atual = datetime.now()
    # Define o caminho de upload como "fotos/nome_objeto/ano/mes/dia/nome_do_arquivo.extensao"
    caminho = os.path.join(nome_objeto, data_atual.strftime('Ano %Y/ Mês %m/ Dia %d'))
    return os.path.join(caminho, f"{filename}.{extensao}")

class Veterinario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome 

class Clinica(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome

class Tutor(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome

class Paciente(models.Model):
    
   
    def data_atual_sem_hora():
        return timezone.now().date()
    def calcular_idade(self):
        today = date.today()
        age_years = today.year - self.nascimento.year
        age_months = today.month - self.nascimento.month
        if today.day < self.nascimento.day:
            age_months -= 1
        if age_months < 0:
            age_years -= 1
            age_months += 12
        return age_years, age_months
    @property
    def idade(self):
        age_years, age_months = self.calcular_idade()
        if age_years == 0:
            return f"{age_months} meses"
        elif age_months == 0:
            return f"{age_years} anos"
        else:
            return f"{age_years} anos e {age_months} meses"
    
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    especie = models.CharField(max_length=100, null=False, blank=False)
    raca_felino = models.ForeignKey(
        to='index.RacaFelino',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="raca_felino_paciente",
    )

    raca_canino = models.ForeignKey(
        to='index.RacaCanino',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="raca_canino_paciente",
    )
    @property
    def raca(self):
        if self.raca_felino:
            return self.raca_felino
        elif self.raca_canino:
            return self.raca_canino
        else:
            return None
        
    nascimento = models.DateField(default=data_atual_sem_hora)
    peso = models.CharField(max_length=100, null=True, blank=True)
    castracao = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    foto = models.ImageField(upload_to=get_upload_path, blank=True)
    tutor = models.ForeignKey(
        Tutor, 
        on_delete=models.CASCADE,
        null=True,
        blank=False, 
        related_name='pacientes'
    )
    
    def __str__(self):
        return self.nome





class RacaFelino(models.Model):
    raca = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.raca

class RacaCanino(models.Model):
    raca = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.raca
    


