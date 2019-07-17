from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hosting
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import HostingTable

# Create your views here.
def hosting(request):
    table = HostingTable(Hosting.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'hosting\hostingList.html', {'table': table})

class HostingCreate(CreateView):
    model = Hosting
    fields = ['empresa', 'server','descricao', 'cpu_mf', 'memoria_mf', 'disco', 'tipo_maq', 'cpu_mv', 'memoria_mv', 'tipo', 'perfil', 'recurso', 'proc_adicional', 'memoria_adicional', 'disco_adicional']
    success_url = reverse_lazy('hosting_list')
    
    def form_valid(self, form):
        form.instance.valor_tabela = valorTabela(form, form.instance.perfil, form.instance.recurso)
        form.instance.valor_disco_adicional = form.instance.disco_adicional * 0.7
        form.instance.valor_memoria_adicional = form.instance.memoria_adicional * 54.9
        form.instance.valor_proc_adicional = form.instance.proc_adicional * 53.5

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        form.instance.hosting = hosting 
        return super(HostingCreate, self).form_valid(form)

def valorTabela(self, perfil, recurso):
        if(perfil == 'GOLD'):
            if(recurso == 'BÁSICO'):
                return 365.62
            if(recurso == 'INTERMEDIÁRIO'):
                return 581.08
            if(recurso == 'AVANÇADO'):
                return 1020.02
        if(perfil == 'PLATINUM'):
            if(recurso == 'BÁSICO'):
                return 548.43
            if(recurso == 'INTERMEDIÁRIO'):
                return 871.62
            if(recurso == 'AVANÇADO'):
                return 1533.04

def hostingCreate(request):
    return render(request, 'hosting\create_hosting.html')




class HostingUpdate(UpdateView):
    model = Hosting
    fields = ['descricao', 'cpu_mf', 'memoria_mf', 'disco', 'tipo_maq', 'cpu_mv', 'memoria_mv',
    'tipo', 'perfil', 'recurso', 'valor_tabela', 'proc_adicional', 'valor_proc_adicional', 
    'valor_proc_adicional', 'memoria_adicional', 'valor_memoria_adicional', 'disco_adicional', 'valor_disco_adicional']
    success_url = reverse_lazy('hosting_list')

class HostingDelete(DeleteView):
    model = Hosting
    success_url = reverse_lazy('hosting_list')