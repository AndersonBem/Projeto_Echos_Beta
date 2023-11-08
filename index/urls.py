from django.urls import path
from index.views import index,lista_veterinarios,lista_clinicas,lista_pacientes,lista_tutores,nova_clinica,novo_paciente,novo_tutor,novo_veterinario, buscar_paciente, buscar_veterinario, buscar_tutor, buscar_clinica

urlpatterns = [
    path('',index, name='index'),
    path('lista_veterinarios/', lista_veterinarios, name='lista_veterinarios'),
    path('lista_clinicas/', lista_clinicas, name='lista_clinicas'),
    path('lista_pacientes/',lista_pacientes, name='lista_pacientes'),
    path('lista_tutores', lista_tutores, name='lista_tutores'),
    path('nova_clinica', nova_clinica, name='nova_clinica'),
    path('novo_paciente', novo_paciente, name='novo_paciente'),
    path('novo_tutor', novo_tutor, name='novo_tutor'),
    path('novo_veterinario', novo_veterinario, name='novo_veterinario'),
    path("buscar_paciente", buscar_paciente, name="buscar_paciente"),
    path("buscar_veterinario", buscar_veterinario, name="buscar_veterinario"),
    path("buscar_tutor", buscar_tutor, name="buscar_tutor"),
    path("buscar_clinica", buscar_clinica, name="buscar_clinica"),
]