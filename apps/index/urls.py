from django.urls import path, include
from .views import DeletarTutorView, DeletarPacienteView, DeletarClinicaView, DeletarVeterinarioView
from apps.index.views import \
    index,lista_veterinarios,lista_clinicas,lista_pacientes,lista_tutores,nova_clinica,novo_paciente,novo_tutor,novo_veterinario, buscar_paciente, buscar_veterinario, buscar_tutor, buscar_clinica,\
    deletar_veterinario,editar_veterinario, deletar_clinica, editar_clinica, deletar_paciente,editar_paciente,editar_tutor, deletar_tutor, selecao,\
    novo_paciente_canino, editar_paciente_canino, deletar_paciente_canino, exibicao,exibicao_tutor, laudo, nova_raca_felino, nova_raca_canino

urlpatterns = [
    path('',index, name='index'),
    path('lista_veterinarios/', lista_veterinarios, name='lista_veterinarios'),
    path('lista_clinicas/', lista_clinicas, name='lista_clinicas'),
    path('lista_pacientes/',lista_pacientes, name='lista_pacientes'),
    path('lista_tutores', lista_tutores, name='lista_tutores'),

    path('nova_clinica', nova_clinica, name='nova_clinica'),
    path('editar_clinica/<int:clinica_id>', editar_clinica, name='editar_clinica'),
    path('deletar_clinica/<int:clinica_id>', deletar_clinica, name='deletar_clinica'),

    path('novo_paciente', novo_paciente, name='novo_paciente'),
    path('editar_paciente/<int:paciente_id>', editar_paciente, name='editar_paciente'),
    path('deletar_paciente/<int:paciente_id>', deletar_paciente, name='deletar_paciente'),

    path('novo_paciente_canino', novo_paciente_canino, name='novo_paciente_canino'),
    path('editar_paciente_canino/<int:paciente_id>', editar_paciente_canino, name='editar_paciente_canino'),
    path('deletar_paciente_canino/<int:paciente_id>', deletar_paciente_canino, name='deletar_paciente_canino'),

    path('novo_tutor', novo_tutor, name='novo_tutor'),
    path('editar_tutor/<int:tutor_id>', editar_tutor, name='editar_tutor'),
    path('deletar_tutor/<int:tutor_id>', deletar_tutor, name='deletar_tutor'),

    path('novo_veterinario', novo_veterinario, name='novo_veterinario'),
    path('editar_veterinario/<int:veterinario_id>', editar_veterinario, name='editar_veterinario'),
    path('deletar_veterinario/<int:veterinario_id>', deletar_veterinario, name='deletar_veterinario'),

    path('buscar_paciente/', buscar_paciente, name='buscar_paciente'),
    path("buscar_paciente/<int:paciente_id>/", buscar_paciente, name="buscar_paciente_com_id"),
    path("buscar_veterinario", buscar_veterinario, name="buscar_veterinario"),
    path("buscar_tutor", buscar_tutor, name="buscar_tutor"),
    path("buscar_clinica", buscar_clinica, name="buscar_clinica"),

    path('selecao/<int:tutor_id>/', selecao, name='selecao'),

    path('exibicao/<int:paciente_id>/', exibicao, name='exibicao'),
    path('exibicao_tutor/<int:tutor_id>/', exibicao_tutor, name='exibicao_tutor'),
    path('tinymce/', include('tinymce.urls')),
    path('laudo/<int:paciente_id>/<int:tutor_id>/',laudo,name='laudo'),

    path('deletar_tutor/<int:pk>/', DeletarTutorView.as_view(), name='deletar_tutor'),
    path('deletar_paciente/<int:pk>/', DeletarPacienteView.as_view(), name='deletar_paciente'),
    path('deletar_clinica/<int:pk>/', DeletarClinicaView.as_view(), name='deletar_clinica'),
    path('deletar_veterinario/<int:pk>/', DeletarVeterinarioView.as_view(), name='deletar_veterinario'),

    path('nova_raca_felino', nova_raca_felino, name='nova_raca_felino'),
    path('nova_raca_canino', nova_raca_canino, name='nova_raca_canino'),
]