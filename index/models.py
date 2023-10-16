from django.db import models
from datetime import datetime

# Create your models here.

class Veterinario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome 

class Clinica(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    endereco = models.TextField(null=False, blank=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome

class Paciente(models.Model):

    OPCOES_CATEGORIA = [
        ("FELINO", "Felino"),
        ("CANINO", "Canino")
    ]

    nome = models.CharField(max_length=100, null=False, blank=False)
    especie = models.CharField(max_length=100,choices=OPCOES_CATEGORIA,default="")
    raca = models.CharField(max_length=150, null=False, blank=False)
    nascimento = models.CharField(max_length=50, null=False, blank=False)
    peso = models.CharField(max_length=5, null=False, blank=False)
    castracao = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    foto = models.ImageField(upload_to="imagem_laudo/%Y/%m/%d", blank=True)
    
    def __str__(self):
        return self.nome

class Tutor(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    endereco = models.TextField(null=False, blank=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome


