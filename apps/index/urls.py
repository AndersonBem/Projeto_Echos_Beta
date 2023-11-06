from django.urls import path
from apps.index.views import \
    index,lista_veterinarios,lista_clinicas,lista_pacientes,lista_tutores,nova_clinica,novo_paciente,novo_tutor,novo_veterinario, buscar_paciente, buscar_veterinario, buscar_tutor, buscar_clinica,\
    deletar_veterinario,editar_veterinario, deletar_clinica, editar_clinica, deletar_paciente,editar_paciente,editar_tutor, deletar_tutor 

urlpatterns = [
    path('',index, name='index'),
    path('lista_veterinarios/', lista_veterinarios, name='lista_veterinarios'),
    path('lista_clinicas/', lista_clinicas, name='lista_clinicas'),
    path('lista_pacientes/',lista_pacientes, name='lista_pacientes'),
    path('lista_tutores', lista_tutores, name='lista_tutores'),

    path('nova_clinica', nova_clinica, name='nova_clinica'),
    path('editar_clinica', editar_clinica, name='editar_clinica'),
    path('deletar_clinica', deletar_clinica, name='deletar_clinica'),

    path('novo_paciente', novo_paciente, name='novo_paciente'),
    path('editar_paciente', editar_paciente, name='editar_paciente'),
    path('deletar_paciente', deletar_paciente, name='deletar_paciente'),

    path('novo_tutor', novo_tutor, name='novo_tutor'),
    path('editar_tutor', editar_tutor, name='editar_tutor'),
    path('deletar_tutor', deletar_tutor, name='deletar_tutor'),

    path('novo_veterinario', novo_veterinario, name='novo_veterinario'),
    path('editar_veterinario', editar_veterinario, name='editar_veterinario'),
    path('deletar_veterinario', deletar_veterinario, name='deletar_veterinario'),

    path("buscar_paciente", buscar_paciente, name="buscar_paciente"),
    path("buscar_veterinario", buscar_veterinario, name="buscar_veterinario"),
    path("buscar_tutor", buscar_tutor, name="buscar_tutor"),
    path("buscar_clinica", buscar_clinica, name="buscar_clinica"),
]