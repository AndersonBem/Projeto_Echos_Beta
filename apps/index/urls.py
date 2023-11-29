from django.urls import path, include
from .views import DeletarTutorView, DeletarPacienteView, DeletarClinicaView, DeletarVeterinarioView
from apps.index.views import \
    index,lista_veterinarios,lista_clinicas,lista_pacientes,lista_tutores,nova_clinica,novo_paciente,novo_tutor,novo_veterinario, buscar_paciente, buscar_veterinario, buscar_tutor, buscar_clinica,\
    deletar_veterinario,editar_veterinario, deletar_clinica, editar_clinica, deletar_paciente,editar_paciente,editar_tutor, deletar_tutor, selecao,\
    novo_paciente_canino, editar_paciente_canino, deletar_paciente_canino, exibicao,exibicao_tutor, laudo, nova_raca_felino, nova_raca_canino,cadastrar_laudo,escolha_exame, obter_frases,nova_frase, exibir_laudo, deletar_laudo, editar_laudo, lista_frases, lista_laudos,deletar_frase, deletar_laudospadrao,\
    editar_frases, editar_laudopadrao, deletar_imagem, adicionar_imagem, export_pdf,exibir_pdf, enviar_pdf, lista_tarefas_agendadas, editar_horario_tarefa, deletar_tarefa,enviar_whatsapp
    

urlpatterns = [
    path('',index, name='index'),
    path('lista_veterinarios/', lista_veterinarios, name='lista_veterinarios'),
    path('lista_clinicas/', lista_clinicas, name='lista_clinicas'),
    path('lista_pacientes/',lista_pacientes, name='lista_pacientes'),
    path('lista_tutores', lista_tutores, name='lista_tutores'),
    path('lista_frases/', lista_frases, name='lista_frases'),
    path('lista_laudos/', lista_laudos, name='lista_laudos'),

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
    path('laudo/<int:paciente_id>/<int:tutor_id>/<int:laudo_id>/',laudo,name='laudo'),

    path('deletar_tutor/<int:pk>/', DeletarTutorView.as_view(), name='deletar_tutor'),
    path('deletar_paciente/<int:pk>/', DeletarPacienteView.as_view(), name='deletar_paciente'),
    path('deletar_clinica/<int:pk>/', DeletarClinicaView.as_view(), name='deletar_clinica'),
    path('deletar_veterinario/<int:veterinario_id>', deletar_veterinario, name='deletar_veterinario'),
    path('deletar_frase/<int:frases_id>', deletar_frase, name='deletar_frase'),
    path('deletar_laudospadrao/<int:laudo_id>', deletar_laudospadrao, name='deletar_laudospadrao'),

    path('nova_raca_felino', nova_raca_felino, name='nova_raca_felino'),
    path('nova_raca_canino', nova_raca_canino, name='nova_raca_canino'),

    path('cadastrar_laudo', cadastrar_laudo, name='cadastrar_laudo'),
    path('escolha_exame',escolha_exame, name='escolha_exame'),

    path('api/frases/', obter_frases, name='obter_frases'),
    path('nova_frase',nova_frase, name='nova_frase'),

    path('exibir_laudo/<int:laudos_paciente_id>/', exibir_laudo, name='exibir_laudo'),

    path('deletar_laudo/<int:laudo_paciente_id>/', deletar_laudo, name='deletar_laudo'),
    path('editar_laudo/<int:laudo_paciente_id>/',editar_laudo, name='editar_laudo'),

    path('editar_frases/<int:frases_id>', editar_frases, name='editar_frases'),
    path('editar_laudopadrao/<int:laudo_id>', editar_laudopadrao, name='editar_laudopadrao'),

    path('deletar_imagem/<int:imagem_id>/', deletar_imagem, name='deletar_imagem'),
    path('adicionar_imagem/<int:laudo_id>/', adicionar_imagem, name='adicionar_imagem'),

    path('export-pdf/<int:laudos_paciente_id>/', export_pdf, name='export-pdf'),
    path('exibir_pdf/<int:laudos_paciente_id>/',exibir_pdf,name='exibir_pdf'),

    path('enviar_pdf/<int:laudos_paciente_id>/',enviar_pdf,name='enviar_pdf'),
    path('tarefas_agendadas/', lista_tarefas_agendadas, name='lista_tarefas_agendadas'),
    path('editar_horario_tarefa/<int:tarefa_id>/', editar_horario_tarefa, name='editar_horario_tarefa'),
    path('deletar_tarefa/<int:tarefa_id>/', deletar_tarefa, name='deletar_tarefa'),
    path('enviar_whatsapp/<int:laudos_paciente_id>/',enviar_whatsapp,name='enviar_whatsapp')
    
]