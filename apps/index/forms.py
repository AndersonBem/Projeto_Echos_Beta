from django import forms

from datetime import date

from apps.index.models import Veterinario, Clinica, Paciente, Tutor, RacaCanino, RacaFelino, Laudo

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
            'endereco': TinyMCE(
                attrs={'cols': 80, 'rows': 30},  # Isso é opcional, ajuste conforme necessário
                mce_attrs={'toolbar': 'bold italic | link | alignleft aligncenter alignright | undo redo |'},
            ),
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
            'laudo': 'Laudo'
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control'}),
            'tutor': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'id': 'peso'}),
            'email_extra': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_extra': forms.TextInput(attrs={'class': 'form-control'}),
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
            'laudo': TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'toolbar': 'bold italic | link | alignleft aligncenter alignright | undo redo |'},
            ),
        }
    data = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), initial=date.today())

    def __init__(self, *args, **kwargs):
        # Aceita um argumento adicional chamado 'tutor'
        tutor = kwargs.pop('tutor', None)
        paciente = kwargs.pop('paciente', None)
        super(LaudoForms, self).__init__(*args, **kwargs)

        # Preenche o campo 'email' com o email do tutor se disponível
        if tutor:
            self.fields['email'].initial = tutor.email

        # Preenche os campos do paciente se disponíveis
        if paciente:
            self.fields['paciente'].initial = paciente.nome
            self.fields['especie'].initial = paciente.especie
            self.fields['raca'].initial = str(paciente.raca_felino) if paciente.raca_felino else str(paciente.raca_canino) if paciente.raca_canino else ''
            self.fields['sexo'].initial = paciente.sexo
            self.fields['peso'].initial = paciente.peso

            # Preenche o campo 'idade' usando o método de propriedade 'idade' do modelo
            self.fields['idade'].initial = str(paciente.idade)

            