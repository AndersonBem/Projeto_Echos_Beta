from django import forms

from multiupload.fields import MultiFileField

from datetime import date, datetime, timedelta

from apps.index.models import Veterinario, Clinica, Paciente, Tutor, RacaCanino, RacaFelino, Laudo, LaudosPadrao, Frases,\
LaudoImagem

from tinymce.widgets import TinyMCE

from django.utils import timezone



class VeterinarioForms(forms.ModelForm):
    class Meta:
        model = Veterinario
        exclude = ['data_criacao']

        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'E-mail'
        } 
        
        widgets={
            'nome' : forms.TextInput(attrs={'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control','data-mask': '(00) 00000-0000', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),

        }

class ClinicaForms(forms.ModelForm):
    class Meta:
        model = Clinica
        exclude = ['data_criacao']

        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'endereco': "Endereço"
        } 
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control',  'data-mask': '(00) 00000-0000', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PacienteForms(forms.ModelForm):
    especie = forms.CharField(initial='Felino')

    class Meta:
        model = Paciente
        exclude = ['data_criacao', 'raca_canino']
        
        labels = {
            'nome': 'Nome',
            'raca_felino': 'Raça Felino',
            'nascimento': "Data de Nascimento",
            'peso': "Peso",
            'castracao': "O paciente é castrado?",
            
            'tutor': "Tutor"
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'raca_felino': forms.Select(attrs={'class': 'radio-select'}),
            'nascimento': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'id': 'peso'}),
            'castracao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'tutor': forms.Select(attrs={'class': 'form-control'})
        }

class PacienteCaninoForms(forms.ModelForm):
    especie = forms.CharField(initial='Canino')

    class Meta:
        model = Paciente
        exclude = ['data_criacao','raca_felino']
        

        labels = {
            'nome': 'Nome',
            'raca_canino': 'Raça Canino',
            'nascimento': "Data de Nascimento",
            'peso': "Peso",
            'castracao': "O paciente é castrado?",
            
            'tutor': "Tutor"
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'raca_canino': forms.Select(attrs={'class': 'radio-select'}),
            'nascimento': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'id': 'peso'}),
            'castracao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'tutor': forms.Select(attrs={'class': 'form-control'})
        }

class TutorForms(forms.ModelForm):
    class Meta:
        model = Tutor
        exclude = ['data_criacao']

        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'endereco': "Endereço"
        } 
        
        widgets={
            'nome' : forms.TextInput(attrs={'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'endereco' : forms.TextInput(attrs={'class':'form-control'})

        }


class LaudoForms(forms.ModelForm):
    laudo_imagem = MultiFileField(min_num=1, max_num=100, required=False)
    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.all().order_by('nome'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # Adicione este campo para controle de exibição condicional
    mostrar_preco = forms.BooleanField(required=False, widget=forms.HiddenInput)



    class Meta:
        model = Laudo
        fields = '__all__'

        labels = {
            'paciente': 'Paciente',
            'especie': 'Especie',
            'raca': 'Raça',
            'sexo': "Sexo",
            'tutor': 'Tutor',
            'email': 'E-mail do Tutor',
            'idade': 'Idade',
            'peso': 'Peso',
            'email_extra': 'E-mail extra',
            'telefone_extra': 'Telefone extra',
            'suspeita': 'Suspeita',
            'clinica': 'Cliníca',
            'veterinario': 'Veterinário',
            'data': 'Data',
            'tipo_laudo': 'Tipo de laudo',
            'laudo': 'Laudo',
            'preco': 'Preço',
            
            
        }

        widgets = {
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'id': 'peso'}),
            'email_extra': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_extra': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000'}),
            'suspeita': forms.TextInput(attrs={'class': 'form-control'}),
            'clinica': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'tipo_laudo': forms.Select(attrs={'class': 'form-control'}),
            
            'laudo':TinyMCE(attrs={'cols': 80, 'rows': 30, 'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'form-control'}),
        
            
        }
    data = forms.DateTimeField(
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d/%m/%Y %H:%M'),
    )

    hora_envio = forms.DateTimeField(
        widget=forms.DateInput(attrs={'class': 'form-control flatpickr'}, format='%d/%m/%Y %H:%M'),
        initial=lambda: timezone.now().replace(hour=1, minute=0, second=0, microsecond=0),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Defina o valor inicial do campo 'data' com base na lógica desejada
        if not self.instance.pk:  # Verifica se é um novo objeto, não uma edição
            self.fields['data'].initial = timezone.now()

        if not self.data.get('mostrar_preco', False):
            # Se o campo 'mostrar_preco' não estiver configurado para True, remova o campo 'preco'
            del self.fields['preco']

    def save(self, commit=True):
        laudo = super(LaudoForms, self).save(commit=False)
        # Faça qualquer processamento adicional aqui, se necessário
        if commit:
            laudo.save()
        return laudo


class RelatorioForm(forms.Form):
    # Obtenha os meses únicos dos laudos existentes formatados
    meses_choices = [(f"{m.strftime('%m/%Y')}", f"{m.strftime('%m/%Y')}") for m in Laudo.objects.dates('data', 'month')]

    mes = forms.ChoiceField(choices=meses_choices)
    dias_trabalhados = forms.IntegerField(min_value=1)

        




class RacaFelinoForms(forms.ModelForm):
    class Meta: 
        model = RacaFelino
        fields = '__all__'

        labels = {
            'raca': 'Raça'
        }

        widgets = {
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
class RacaCaninoForms(forms.ModelForm):
    class Meta: 
        model = RacaCanino
        fields = '__all__'

        labels = {
            'raca': 'Raça'
        }

        widgets = {
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LaudoPadraoForms(forms.ModelForm):
    class Meta:
        model = LaudosPadrao
        fields = '__all__'

        labels = {
            'nome_exame': 'Nome do Exame',
            'tipo_exame': 'Tipo do Exame',
            'laudo': "Laudo padrão"
        }

        widgets = {
            'nome_exame': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_exame': forms.TextInput(attrs={'class': 'form-control'}),
            'laudo': TinyMCE(attrs={'cols': 80, 'rows': 30,'class': 'form-control'}),
        }


class FrasesForm(forms.ModelForm):
    class Meta:
        model = Frases
        fields = '__all__' 

        labels = {
            'tipo': "Tipo",
            'palavra_chave': "Palavras chave",
            'texto': 'Frase padrão',
        }

        widgets = {
            'tipo': TinyMCE(attrs={'cols': 40, 'rows': 1}),
            'palavra_chave': TinyMCE(attrs={'cols': 40, 'rows': 1}),
            'texto': TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }


class NovaImagemForm(forms.ModelForm):
    laudo_imagem = MultiFileField(min_num=1, max_num=100)
    class Meta:
        model = LaudoImagem
        fields = ['laudo_imagem']



