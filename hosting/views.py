from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hosting, Servicos_adicionais, Backup_dados
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import HostingTable, SimpleTable
from django.shortcuts import redirect
import django_tables2
import datetime
from django.core import serializers
from django.http import HttpResponseRedirect

# Create your views here.
def add_client(request):
    return render(request, 'hosting/add_client.html')

def hostingFieb(request):
    data = datetime.date.today().strftime("%B")
    hosting_list = []
    date = datetime.date(year = 2000, month= 1, day = 1)
    for item in Hosting.objects.all():
        if item.hosting_fieb & (item.data_delete==date):
            hosting_list.append(item)
    total= 0
    list_dic = []
    total_empresa = 0
    todas_empresas = []

    for item in hosting_list:
        todas_empresas.append(item.empresa)

    for i in empresas(todas_empresas) :
        dic = {}
        dic['empresa'] = i
        total_empresa = 0
        for item in hosting_list :
            if(i == item.empresa) :
                total_empresa = item.valor_total + total_empresa
        dic['valor'] = total_empresa
        list_dic.append(dic)

    for item in hosting_list :
        total = item.valor_total + total


    return render(request, 'hosting/hosting_fieb.html', {'mes': data, 'total': total, 'totalAno': total*12,'total_empresa': list_dic, 'hosting_list': hosting_list, 'tabela': 'SENAI'})

def servicos_adicionais(request):
    data = datetime.date.today().strftime("%B")
    servico_list = []
    backup_list = []
    date = datetime.date(year = 2000, month= 1, day = 1)

    for item in Servicos_adicionais.objects.all():
        if (item.data_delete==date):
            servico_list.append(item)

    for item in Backup_dados.objects.all():
        if (item.data_delete==date):
            backup_list.append(item)

    total_servico = 0
    total_backup = 0
    total_casa_senai = 0
    total_casa_fieb = 0
    total_casa_sesi = 0
    total_casa_iel = 0
    for item in backup_list :
        print(item.data_delete)
        if(item.casa == 'SENAI') & (item.data_delete==date) :
            total_casa_senai = item.valor + total_casa_senai
        if(item.casa == 'FIEB') & (item.data_delete==date) :
            total_casa_fieb = item.valor + total_casa_fieb
        if(item.casa == 'SESI') & (item.data_delete==date) :
            total_casa_sesi = item.valor + total_casa_sesi
        if(item.casa == 'IEL') & (item.data_delete==date) :
            total_casa_iel = item.valor + total_casa_iel
        total_backup = item.valor + total_backup

    for item in servico_list :
        if(item.casa == 'SENAI') & (item.data_delete==date) :
            total_casa_senai = item.valor + total_casa_senai
        if(item.casa == 'FIEB') & (item.data_delete==date) :
            total_casa_fieb = item.valor + total_casa_fieb
        if(item.casa == 'SESI') & (item.data_delete==date) :
            total_casa_sesi = item.valor + total_casa_sesi
        if(item.casa == 'IEL') & (item.data_delete==date) :
            total_casa_iel = item.valor + total_casa_iel
        total_servico = item.valor + total_servico
    
    return render(request, 'hosting/servicos.html', {'mes': data, 'total_servico': total_servico, 'total_backup': total_backup, 'total_adicionais': total_servico + total_backup, 'casa_senai': total_casa_senai, 'casa_sesi': total_casa_sesi, 'casa_fieb': total_casa_fieb, 'casa_iel': total_casa_iel, 'backup_list': backup_list, 'servico_list': servico_list})

def redirectSenai(request):
    return redirect('hosting_list')

def tabelaPrecos(request):
    data = datetime.date.today().strftime("%B")
    return render(request, 'hosting/tabela_preco.html', {'data': data})

def empresas(todas_empresas):
    emp = []
    for item in todas_empresas:
        if(emp is None):
            emp.append(item)
        if(emp.count(item) == 0 ):
            emp.append(item)
    return emp

def financeiroSENAI(request):
    data = datetime.date.today().strftime("%B")
    hosting_list = []

    for item in Hosting.objects.all():
        if item.hosting_senai:
            hosting_list.append(item)

    list_dic = []
    total_empresa = 0
    todas_empresas = []
    for item in hosting_list:
        todas_empresas.append(item.empresa)

    for i in empresas(todas_empresas) :
        dic = {}
        dic['empresa'] = i
        total_empresa = 0
        for item in hosting_list :
            if(i == item.empresa) :
                total_empresa = item.valor_total + total_empresa
        dic['valor'] = total_empresa
        list_dic.append(dic)



    return render(request, 'hosting/financeiro_senai.html', {'data': data, 'valor_empresa': list_dic, 'tabela': 'SENAI'})

def historico(request):
    hosting_list_mes1 = []
    hosting_list_mes2 = []
    hosting_list_mes3 = []
    mes1 = None
    mes2 = None
    mes3 = None
    for item in Hosting.objects.all():
        if abs(item.data_insert - datetime.date.today().month)<=3 :
            if abs(item.data_insert - datetime.date.today().month) == 1 :
                mes1 = item.data_insert.strftime("%B")
                hosting_list_mes1.append(item)
            if abs(item.data_insert - datetime.date.today().month) == 2 :
                mes2 = item.data_insert.strftime("%B")
                hosting_list_mes2.append(item)
            if abs(item.data_insert - datetime.date.today().month) == 3 :
                mes3 = item.data_insert.strftime("%B")
                hosting_list_mes3.append(item)

    return render(request, 'hosting/financeiro_senai.html', {'mes1': mes1, 'mes2': mes2, 'mes3': mes3, 'hosting1': hosting_list_mes1,'hosting2': hosting_list_mes2,'hosting3': hosting_list_mes3})

class HostingList(ListView):
    model = Hosting
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HostingList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the 
        hosting_list = []
        date = datetime.date(year = 2000, month= 1, day = 1)
        for item in Hosting.objects.all():
            print(item.data_delete)
            if item.hosting_senai & (item.data_delete==date):
                hosting_list.append(item)

        #colocar todos os meses no contex
        #tentar pegar em qual mes foi clicado no ajax
        #sabendo qual mes foi clicado, reexibir as tabelas para o mes selecionado
        #colocar os 12 meses


        context['mes'] = datetime.date.today().strftime("%B")
        context['hosting_list'] = hosting_list
        total= 0
        list_dic = []
        total_empresa = 0
        todas_empresas = []
        for item in context['hosting_list']:
            todas_empresas.append(item.empresa)

        for i in empresas(todas_empresas) :
            dic = {}
            dic['empresa'] = i
            total_empresa = 0
            for item in context['hosting_list'] :
                if(i == item.empresa) :
                    total_empresa = item.valor_total + total_empresa
            dic['valor'] = total_empresa
            list_dic.append(dic)

        for item in context['hosting_list'] :
            total = item.valor_total + total

        context['total'] = total
        context['totalAno'] = total*12
        context['total_empresa'] = list_dic
        context['tabela'] = 'SENAI'
        # context['teste'] = "teste"
        return context

class HostingCreate(CreateView):
    model = Hosting
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'tipo_maq', 'perfil', 'hosting_senai', 'hosting_fieb']
    success_url = reverse_lazy('hosting_list')

    def form_valid(self, form):
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
        form.instance.empresa = form.instance.empresa.upper()
        form.instance.tipo_maq = form.instance.tipo_maq.capitalize()
        form.instance.tipo = tipo(form.instance.cpu, form.instance.memoria)
        form.instance.recurso = recurso(form.instance.tipo)
        form.instance.perfil = form.instance.perfil.upper()
        form.instance.valor_tabela = valorTabela(form, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = mem_adicional(form.instance.tipo, form.instance.memoria)
        form.instance.proc_adicional = cpu_adicional(form.instance.tipo, form.instance.cpu)
        form.instance.disco_adicional = disc_adicional(form.instance.disco)

        if(form.instance.disco_adicional > 0):
            form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 0.704, 2)
        else:
            form.instance.valor_disco_adicional = 0
        if(form.instance.memoria_adicional > 0):
            form.instance.valor_memoria_adicional =  round(form.instance.memoria_adicional * 54.904, 2)
        else:
            form.instance.valor_memoria_adicional = 0
        if(form.instance.proc_adicional > 0):
            form.instance.valor_proc_adicional =  round(form.instance.proc_adicional * 53.512, 2)
        else:
            form.instance.valor_proc_adicional = 0

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingCreate, self).form_valid(form)

def disc_adicional(disco):
    return disco - 80

def mem_adicional(tipo, mem):
    if(tipo == 2):
        return mem - 8
    if(tipo == 3):
        return mem - 16
    else:
        return mem - 4

def cpu_adicional(tipo, cpu):
    if(tipo == 2):
        return cpu - 4
    if(tipo == 3):
        return cpu - 8
    else:
        return cpu - 2

def recurso(tipo):
    if(tipo == 1):
        return 'BÁSICO'
    if(tipo == 2):
        return 'INTERMEDIÁRIO'
    else:
        return 'AVANÇADO'

def valorTabela(self, perfil, recurso):
    if(perfil == 'GOLD'):
        if(recurso == 'BÁSICO'):
            return 365.62
        if(recurso == 'INTERMEDIÁRIO'):
            return 581.08
        if(recurso == 'AVANÇADO'):
            return 1022.02
    if(perfil == 'PLATINUM'):
        if(recurso == 'BÁSICO'):
            return 548.43
        if(recurso == 'INTERMEDIÁRIO'):
            return 871.62
        if(recurso == 'AVANÇADO'):
            return 1533.04

def tipo(cpu, mem):
    tipo_cpu = 1
    tipo_mem = 1
    if(cpu > 6):
        tipo_cpu = 3
    elif(cpu<=3):
       tipo_cpu = 1
    else:
        tipo_cpu = 2
    if(mem > 12):
        tipo_mem = 3
    elif(mem <= 6):
        tipo_mem = 1
    else:
        tipo_mem = 2
    
    if(tipo_cpu > tipo_mem):
        return tipo_cpu
    else:
        return tipo_mem

def hostingCreate(request):
    return render(request, 'hosting\create_hosting.html')

class HostingUpdate(UpdateView):
    model = Hosting
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'tipo_maq', 'perfil', 'hosting_senai', 'hosting_fieb']
    success_url = reverse_lazy('hosting_list')
    
    def form_valid(self, form):
        form.instance.empresa = form.instance.empresa.upper()
        form.instance.tipo_maq = form.instance.tipo_maq.capitalize()
        form.instance.tipo = tipo(form.instance.cpu, form.instance.memoria)
        form.instance.recurso = recurso(form.instance.tipo)
        form.instance.perfil = form.instance.perfil.upper()
        form.instance.valor_tabela = valorTabela(form, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = mem_adicional(form.instance.tipo, form.instance.memoria)
        form.instance.proc_adicional = cpu_adicional(form.instance.tipo, form.instance.cpu)
        form.instance.disco_adicional = disc_adicional(form.instance.disco)

        if(form.instance.disco_adicional > 0):
            form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 0.704, 2)
        else:
            form.instance.valor_disco_adicional = 0
        if(form.instance.memoria_adicional > 0):
            form.instance.valor_memoria_adicional = round(form.instance.memoria_adicional * 54.904, 2)
        else:
            form.instance.valor_memoria_adicional = 0
        if(form.instance.proc_adicional > 0):
            form.instance.valor_proc_adicional = round(form.instance.proc_adicional * 53.512, 2)
        else:
            form.instance.valor_proc_adicional = 0

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingUpdate, self).form_valid(form)

class HostingDelete(DeleteView):
    model = Hosting
    success_url = reverse_lazy('hosting_list')
    def post(self, request, *args, **kwargs): 
        if self.request.POST.get("confirm_delete"):
            # when confirmation page has been displayed and confirm button pressed
            path = self.request.path
            id = path.split('/')
            delete_item = Hosting.objects.get(id = id[2])
            delete_item.data_delete = datetime.date.today()
            delete_item.save()
            print(delete_item.data_delete,end='\n')
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(self.success_url)
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)

class Sevicos_adicionaisCreate (CreateView):
    model = Servicos_adicionais
    fields = ['casa', 'descricao', 'ticket','duracao', 'observacao', 'responsavel', 'valor']
    success_url = reverse_lazy('servicos')
    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        return super(Sevicos_adicionaisCreate, self).form_valid(form)

class Servicos_adicionaisUpdate(UpdateView):
    model = Servicos_adicionais
    fields = ['casa', 'descricao', 'ticket','duracao', 'observacao', 'responsavel', 'valor']
    success_url = reverse_lazy('servicos')
    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        return super(Servicos_adicionaisUpdate, self).form_valid(form)

class Servicos_adicionaisDelete(DeleteView):
    model = Servicos_adicionais
    success_url = reverse_lazy('hosting_list')

class Backup_dadosCreate(CreateView):
    model = Backup_dados
    fields = ['casa', 'descricao', 'valorUnitario','volume', 'quantidade']
    success_url = reverse_lazy('servicos')

    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        if(form.instance.quantidade == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.volume
        if(form.instance.volume == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.quantidade
        return super(Backup_dadosCreate, self).form_valid(form)

class Backup_dadosUpdate(UpdateView):
    model = Backup_dados
    fields = ['casa', 'descricao', 'valorUnitario','volume', 'quantidade']
    success_url = reverse_lazy('servicos')
    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        if(form.instance.quantidade == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.volume
        if(form.instance.volume == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.quantidade
        return super(Backup_dadosUpdate, self).form_valid(form)

class Backup_dadosDelete(DeleteView):
    model = Backup_dados
    success_url = reverse_lazy('hosting_list')
