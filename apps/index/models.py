from django.db import models
from datetime import datetime, date
from django.utils import timezone
import os
from tinymce.models import HTMLField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from decimal import Decimal


from multiupload.fields import MultiFileField


# Create your models here.

def get_upload_path(instance, filename):
    # Obtém o nome do objeto
    nome_objeto = instance.laudo.paciente.nome
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
    
    class Meta:
        ordering = ['nome']

class Clinica(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']

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
    def castracao_display(self):
        return "Castrado" if self.castracao else "Inteiro"
    
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
        if self.nascimento is None or self.nascimento == "":
            return "Idade não informada"
        
        today = date.today()
        delta = today - self.nascimento
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f"{years} anos e {months} mês(es)" if years > 0 else f"{months} mês(es)"
    
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
        
    nascimento = models.DateField(null=True, blank=True)
    peso = models.CharField(max_length=100, null=True, blank=True)
    castracao = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    tutor = models.ForeignKey(
        'Tutor',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
        related_name='pacientes'
    )
    
    observacao = models.CharField(max_length=200, null=True, blank=True)

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
    
    class Meta:
        ordering = ['raca']

class RacaCanino(models.Model):
    raca = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.raca
    
    class Meta:
        ordering = ['raca']
    

class FormaDePagamento(models.Model):
    forma_de_pagamento = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.forma_de_pagamento

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
    email = models.CharField(max_length=100, null=True, blank=True)
    idade = models.CharField(max_length=100, null=True, blank=True)
    
    peso = models.CharField(max_length=100, null=True, blank=True)
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
    data = models.DateTimeField()
    tipo_laudo = models.ForeignKey(
        to='index.LaudosPAdrao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nome_laudo",
    )
    
    laudo = HTMLField(null=True)

    hora_envio = models.DateTimeField(default=timezone.now().replace(hour=1, minute=0, second=0, microsecond=0),null=True, blank=True)

    preco = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    entregue_whats = models.BooleanField(default=False)
    
    entregue_email = models.BooleanField(default=False)

    laudo_pronto = models.BooleanField(default=False)

    preco_real= models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)

    data_pagamento = models.CharField(max_length=100, null=True, blank=True)

    nota_fiscal = models.BooleanField(default=False)

    observacao_pagamento = models.CharField(max_length=200, null=True, blank=True)

    forma_pagamento = models.ForeignKey(
        FormaDePagamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='laudos_forma_pagamento'
    )

    def save(self, *args, **kwargs):
        # Se a data ainda não foi definida, configure-a para a data e hora atuais
        if not self.data:
            self.data = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # Retorna a representação em string da instância do modelo
        return self.data.strftime('%d%m%Y')





class LaudoImagem(models.Model):
    image = models.FileField('Arquivos', upload_to=get_upload_path, null=True, blank=True)
    laudo = models.ForeignKey(
        Laudo,
        related_name='laudo_imagem',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.laudo.paciente)



class LaudosPadrao(models.Model):
    nome_exame = models.CharField(max_length=100, null=False, blank=False)
    tipo_exame = models.CharField(max_length=100, null=False, blank=False)
    laudo = HTMLField(null=True)

    def __str__(self):
        return self.nome_exame

class Frases(models.Model):
    tipo = HTMLField(null=True)
    palavra_chave = HTMLField(null=True)
    texto = HTMLField(null=True)

    def __str__(self):
        return self.tipo


class Inventario(models.Model):
    
    alcool = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    gel_usg = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    seringa_10ml = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    seringa_5ml = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    seringa_3ml = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    agulha_azul = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    cateter_azul = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    cateter_rosa = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    gaze_n_esteril = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    pano_de_campo = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    essencia_spray = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    papel_quadrado = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    desinfetante_herbal = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    prope = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    seringa_60ml = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    scal_azul = models.DecimalField(max_digits=8, decimal_places=1, default=Decimal('0.0'))
    
    def save(self, *args, **kwargs):
        if Inventario.objects.exists():
            # Se já existe uma instância, atualiza seus valores
            existing_inventario = Inventario.objects.first()
            self.id = existing_inventario.id  # Garante que há apenas uma instância
        super().save(*args, **kwargs)
