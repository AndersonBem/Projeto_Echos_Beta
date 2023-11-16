# mixins.py

from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

class ConfirmacaoMixin(View):
    template_name = 'confirmacao_deletar.html'

    def get_context_data(self, **kwargs):
        return {'objeto': self.objeto}

    def confirmar_delecao(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.objeto.delete()
            return redirect(self.success_url)
        return render(request, self.template_name, self.get_context_data(**kwargs))
