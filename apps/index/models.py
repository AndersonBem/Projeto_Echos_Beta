from django.db import models
from datetime import datetime, date
from django.utils import timezone
import os
from tinymce.models import HTMLField
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from multiupload.fields import MultiFileField


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
    GENERO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]

    @property
    def data_atual_sem_hora(self):
        return timezone.now().strftime('%d/%m/%Y')
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
        today = date.today()
        delta = today - self.nascimento
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f"{years} anos e {months} meses" if years > 0 else f"{months} meses"
    
    @property
    def nascimento_formatado(self):
        return self.nascimento.strftime('%d/%m/%Y')
    
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    especie = models.CharField(max_length=100, null=False, blank=False)
    sexo =  models.CharField(max_length=5, choices=GENERO_CHOICES, default='Macho')
    raca_felino = models.ForeignKey(
        to='index.RacaFelino',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="raca_felino_paciente",
    )

    raca_canino = models.ForeignKey(
        to='index.RacaCanino',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    foto = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    tutor = models.ForeignKey(
        'Tutor',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
        related_name='pacientes'
    )
    
    def __str__(self):
        return self.nome
    
    @receiver(pre_delete, sender='index.Tutor')
    def set_default_tutor(sender, instance, **kwargs):
        default_tutor = Tutor.objects.get(nome='Sem tutor')  # Substitua com a consulta correta
        Paciente.objects.filter(tutor=instance).update(tutor=default_tutor)


class RacaFelino(models.Model):
    raca = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.raca

class RacaCanino(models.Model):
    raca = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.raca
    


class Laudo(models.Model):
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE,
        null=True,
        blank=False, 
        related_name='laudos'
    )
    especie = models.CharField(max_length=100, null=False, blank=False)
    raca = models.CharField(max_length=100, null=True, blank=False)
    sexo = models.CharField(max_length=100, null=True, blank=False)
    tutor = models.ForeignKey(
        'index.Tutor', 
        on_delete=models.CASCADE,
        null=True,
        blank=False, 
        related_name='tutor'
    )
    email = models.CharField(max_length=100, null=True, blank=False)
    idade = models.CharField(max_length=100, null=True, blank=False)
    
    peso = models.CharField(max_length=100, null=True, blank=False)
    email_extra = models.CharField(max_length=100, null=True, blank=True)
    telefone_extra = models.CharField(max_length=100, null=True, blank=True)
    suspeita = models.CharField(max_length=100, null=True, blank=True)
    clinica = models.ForeignKey(
        Clinica, 
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
        related_name='clinicas'
    )
    veterinario = models.ForeignKey(
        Veterinario, 
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
        related_name='pacientes'
    )
    data = models.DateTimeField(default=datetime.now, blank=False)
    tipo_laudo = models.ForeignKey(
        to='index.LaudosPAdrao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tipo_laudo",
    )
    
    laudo = HTMLField(null=True)


class LaudosPadrao(models.Model):
    nome_exame = models.CharField(max_length=100, null=False, blank=False)
    tipo_exame = models.CharField(max_length=100, null=False, blank=False)
    laudo = HTMLField(null=True)

    def __str__(self):
        return self.nome_exame

class Frases(models.Model):
    texto = HTMLField(null=True)

