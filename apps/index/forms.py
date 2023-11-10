from django import forms

from apps.index.models import Veterinario, Clinica, Paciente, Tutor, PacienteCanino, Raca

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
        
        widgets={
            'nome' : forms.TextInput(attrs={'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'endereco' : forms.TextInput(attrs={'class':'form-control'})

        }

class PacienteForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        especie = kwargs.pop('especie', None)
        super(PacienteForms, self).__init__(*args, **kwargs)

        if especie:
            self.fields['raca'].queryset = Raca.objects.filter(especie=especie)

    class Meta:
        model = Paciente
        exclude = ['data_criacao']

        labels = {
            'nome': 'Nome',
            'raca': 'Raça',
            'nascimento': "Data de Nascimento",
            'peso': "Peso",
            'castracao': "O paciente é castrado?",
            'foto': "Foto",
            'tutor': "Tutor"
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.Select(attrs={'class': 'radio-select'}),
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
    class Meta:
        model = PacienteCanino
        exclude = ['data_criacao']

        labels = {
            'nome': 'Nome',
            
            'raca': 'Raça',
            'nascimento': "Data de Nascimento",
            'peso': "Peso",
            'castracao': "O paciente é castrado?",
            'foto': "Foto",
            'tutor': "Tutor"
        } 
        
        widgets={
            'nome' : forms.TextInput(attrs={'class':'form-control'}),
            
            'raca': forms.Select(attrs={'class': 'radio-select'}),
            'nascimento': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'id': 'peso'}),
            'castracao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto' : forms.FileInput(attrs={'class': 'form-control'}),
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
