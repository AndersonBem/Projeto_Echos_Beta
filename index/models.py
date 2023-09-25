from django.db import models

# Create your models here.

class Veterinario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    
    def __str__(self):
        return f"Veterinario [nome={self.nome}]" 

class Clinica(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    endereco = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return f"Cliníca [nome={self.nome}]"

class Paciente(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    especie = models.CharField(max_length=100, null=False, blank=False)
    raca = models.CharField(max_length=150, null=False, blank=False)
    nascimento = models.CharField(max_length=50, null=False, blank=False)
    peso = models.CharField(max_length=5, null=False, blank=False)
    castracao = models.CharField(max_length=2, null=False, blank=False)
    
    def __str__(self):
        return f"Paciente [nome={self.nome}]"

class Tutor(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    endereco = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return f"Tutor [nome={self.nome}]"


