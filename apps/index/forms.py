from django import forms

from multiupload.fields import MultiFileField

from datetime import date

from apps.index.models import Veterinario, Clinica, Paciente, Tutor, RacaCanino, RacaFelino, Laudo, LaudosPadrao, Frases,\
LaudoImagem

from tinymce.widgets import TinyMCE



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
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'telefone'}),
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
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'telefone'}),
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
            'foto': "Foto",
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
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
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
            'foto': "Foto",
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
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
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
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'endereco' : forms.TextInput(attrs={'class':'form-control'})

        }


class LaudoForms(forms.ModelForm):
    laudo_imagem = MultiFileField(min_num=1, max_num=100)
    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

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
            'data': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'tipo_laudo': forms.Select(attrs={'class': 'form-control'}),
            
            'laudo':TinyMCE(attrs={'cols': 80, 'rows': 50, 'class': 'form-control'}),
        }
    data = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), initial=date.today())




        



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
            'laudo': TinyMCE(attrs={'cols': 80, 'rows': 10}),
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

