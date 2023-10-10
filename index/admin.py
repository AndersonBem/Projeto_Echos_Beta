from django.contrib import admin
from index.models import Veterinario, Clinica, Paciente, Tutor

class ListandoVeterinario(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "email")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_per_page = 10
    

class ListandoClinica(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "email", "endereco")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_per_page = 10

class ListandoPaciente(admin.ModelAdmin):
    list_display = ("id", "nome","especie", "raca", "nascimento", "peso", "castracao")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("especie",)
    list_per_page = 10

class ListandoTutor(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "email", "endereco")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_per_page = 10




# Register your models here.



admin.site.register(Veterinario, ListandoVeterinario)
admin.site.register(Clinica, ListandoClinica)
admin.site.register(Paciente, ListandoPaciente)
admin.site.register(Tutor, ListandoTutor)
