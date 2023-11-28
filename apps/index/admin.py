from django.contrib import admin
from apps.index.models import Veterinario, Clinica, Paciente, Tutor, RacaFelino, RacaCanino, Laudo, LaudosPadrao, Frases, LaudoImagem


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
    list_display = ("id", "nome","especie", "raca", "peso", "castracao", "tutor")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("especie",)
    list_per_page = 10

class ListandoTutor(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "email", "endereco")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_per_page = 10

class ListandoRacaFelino(admin.ModelAdmin):
    list_display = ("id", "raca")
    list_display_links = ("id", "raca")
    search_fields = ("raca",)
    list_per_page = 10

class ListandoRacaCanino(admin.ModelAdmin):
    list_display = ("id", "raca")
    list_display_links = ("id", "raca")
    search_fields = ("raca",)
    list_per_page = 10



class ListandoLaudo(admin.ModelAdmin):
    list_display = (
        "id", "tipo_laudo", "paciente", "especie", "raca", "sexo", "tutor", "email", "idade", "peso",
        "email_extra", "telefone_extra", "suspeita", "clinica", "veterinario", "data"
    )
    list_display_links = ("id", "paciente")
    search_fields = ("raca",)
    list_per_page = 100
    


class ListandoLaudoPadrao(admin.ModelAdmin):
    list_display = ("id", "nome_exame","tipo_exame",)
    list_display_links = ("id",)
    search_fields = ("raca","nome_exame")
    list_per_page = 10

class ListandoFrase(admin.ModelAdmin):
    list_display = ("id", "texto", "tipo", "palavra_chave")
    list_display_links = ("id", "texto")
    search_fields = ("id", "texto")
    list_per_page = 10






# Register your models here.







admin.site.register(Veterinario, ListandoVeterinario)
admin.site.register(Clinica, ListandoClinica)
admin.site.register(Paciente, ListandoPaciente)
admin.site.register(Tutor, ListandoTutor)
admin.site.register(RacaFelino, ListandoRacaFelino)
admin.site.register(RacaCanino, ListandoRacaCanino)
admin.site.register(Laudo, ListandoLaudo)
admin.site.register(LaudosPadrao, ListandoLaudoPadrao)
admin.site.register(Frases, ListandoFrase)
admin.site.register(LaudoImagem)
