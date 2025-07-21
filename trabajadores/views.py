from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Trabajador
from .forms import TrabajadorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class TrabajadorListView(LoginRequiredMixin, ListView):
    model = Trabajador
    template_name = 'trabajadores/list.html'
    context_object_name = 'trabajadores'

    def get_queryset(self):
        return Trabajador.objects.filter(eliminado=False)

class TrabajadorCreateView(LoginRequiredMixin, CreateView):
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'trabajadores/form.html'
    success_url = reverse_lazy('trabajadores:listar')

    def form_valid(self, form):
        messages.success(self.request, 'Trabajador agregado correctamente.')
        return super().form_valid(form)

class TrabajadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'trabajadores/form.html'
    success_url = reverse_lazy('trabajadores:listar')

    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente.')
        return super().form_valid(form)

class TrabajadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Trabajador
    template_name = 'trabajadores/confirm_delete.html'
    success_url = reverse_lazy('trabajadores:listar')

    def post(self, request, *args, **kwargs):
        trabajador = self.get_object()
        trabajador.eliminado = True
        trabajador.save()
        messages.success(request, 'Trabajador eliminado suavemente.')
        return redirect(self.success_url)

