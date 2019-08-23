from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hosting, Servicos_adicionais, Backup_dados, Unidades
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
    data = datetime.date.today().strftime("%B - %Y")
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
    data = datetime.date.today().strftime("%B - %Y")
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
    data = datetime.date.today().strftime("%B - %Y")
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
    data = datetime.date.today().strftime("%B - %Y")
    anos = []
    valor_mes = {'jan': 0,'fev': 0,'mar': 0,'abr': 0,'maio': 0,'jun': 0,'jul': 0,'ago': 0,'set': 0,'out': 0,'nov': 0,'dez': 0}
    valor_mes_nead = {'jan': 0,'fev': 0,'mar': 0,'abr': 0,'maio': 0,'jun': 0,'jul': 0,'ago': 0,'set': 0,'out': 0,'nov': 0,'dez': 0}
    valor_mes_servicos = {'jan': 0,'fev': 0,'mar': 0,'abr': 0,'maio': 0,'jun': 0,'jul': 0,'ago': 0,'set': 0,'out': 0,'nov': 0,'dez': 0}
    valor_mes_total = {'jan': 0,'fev': 0,'mar': 0,'abr': 0,'maio': 0,'jun': 0,'jul': 0,'ago': 0,'set': 0,'out': 0,'nov': 0,'dez': 0}
    anos = get_years()
    total_user = 0
    uni = []

    print(request.POST)

    if request.POST  :
        for item in Unidades.objects.all() :
            total_user += item.qtd_user
            
        for item in Backup_dados.objects.filter(casa='SENAI'):
            for ano in anos :
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year and item.data_delete == datetime.date(year = 2000, month= 1, day = 1) :
                    if item.data_insert.month == 1 and 1 <= datetime.date.today().month:
                        valor_mes_servicos['jan'] += item.valor
                    if item.data_insert.month <= 2 and 2 <= datetime.date.today().month:
                        valor_mes_servicos['fev'] += item.valor
                    if item.data_insert.month <= 3 and 3 <= datetime.date.today().month:
                        valor_mes_servicos['mar'] += item.valor
                    if item.data_insert.month <= 4 and 4 <= datetime.date.today().month:
                        valor_mes_servicos['abr'] += item.valor
                    if item.data_insert.month <= 5 and 5 <= datetime.date.today().month:
                        valor_mes_servicos['maio'] += item.valor
                    if item.data_insert.month <= 6 and 6 <= datetime.date.today().month:
                        valor_mes_servicos['jun'] += item.valor
                    if item.data_insert.month <= 7 and 7 <= datetime.date.today().month:
                        valor_mes_servicos['jul'] += item.valor
                    if item.data_insert.month <= 8 and 8 <= datetime.date.today().month:
                        valor_mes_servicos['ago'] += item.valor
                    if item.data_insert.month <= 9 and 9 <= datetime.date.today().month:
                        valor_mes_servicos['set'] += item.valor
                    if item.data_insert.month <= 10 and 10 <= datetime.date.today().month:
                        valor_mes_servicos['out'] += item.valor
                    if item.data_insert.month <= 11 and 11 <= datetime.date.today().month:
                        valor_mes_servicos['nov'] += item.valor
                    if item.data_insert.month <= 12 and 12 <= datetime.date.today().month:
                        valor_mes_servicos['dez'] += item.valor

        for item in Servicos_adicionais.objects.filter(casa='SENAI'):
            for ano in anos :
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year and item.data_delete == datetime.date(year = 2000, month= 1, day = 1) :
                    if item.data_insert.month == 1 and 1 <= datetime.date.today().month:
                        valor_mes_servicos['jan'] += item.valor
                    if item.data_insert.month <= 2 and 2 <= datetime.date.today().month:
                        valor_mes_servicos['fev'] += item.valor
                    if item.data_insert.month <= 3 and 3 <= datetime.date.today().month:
                        valor_mes_servicos['mar'] += item.valor
                    if item.data_insert.month <= 4 and 4 <= datetime.date.today().month:
                        valor_mes_servicos['abr'] += item.valor
                    if item.data_insert.month <= 5 and 5 <= datetime.date.today().month:
                        valor_mes_servicos['maio'] += item.valor
                    if item.data_insert.month <= 6 and 6 <= datetime.date.today().month:
                        valor_mes_servicos['jun'] += item.valor
                    if item.data_insert.month <= 7 and 7 <= datetime.date.today().month:
                        valor_mes_servicos['jul'] += item.valor
                    if item.data_insert.month <= 8 and 8 <= datetime.date.today().month:
                        valor_mes_servicos['ago'] += item.valor
                    if item.data_insert.month <= 9 and 9 <= datetime.date.today().month:
                        valor_mes_servicos['set'] += item.valor
                    if item.data_insert.month <= 10 and 10 <= datetime.date.today().month:
                        valor_mes_servicos['out'] += item.valor
                    if item.data_insert.month <= 11 and 11 <= datetime.date.today().month:
                        valor_mes_servicos['nov'] += item.valor
                    if item.data_insert.month <= 12 and 12 <= datetime.date.today().month:
                        valor_mes_servicos['dez'] += item.valor


        for item in Hosting.objects.filter(hosting_senai='True'):
            for ano in anos :
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year and item.data_delete == datetime.date(year = 2000, month= 1, day = 1) :
                    if item.data_insert.month == 1 and 1 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jan'] += item.valor_total
                        valor_mes['jan'] += item.valor_total
                    if item.data_insert.month <= 2 and 2 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['fev'] += item.valor_total
                        valor_mes['fev'] += item.valor_total
                    if item.data_insert.month <= 3 and 3 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['mar'] += item.valor_total
                        valor_mes['mar'] += item.valor_total
                    if item.data_insert.month <= 4 and 4 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['abr'] += item.valor_total
                        valor_mes['abr'] += item.valor_total
                    if item.data_insert.month <= 5 and 5 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['maio'] += item.valor_total
                        valor_mes['maio'] += item.valor_total
                    if item.data_insert.month <= 6 and 6 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jun'] += item.valor_total
                        valor_mes['jun'] += item.valor_total
                    if item.data_insert.month <= 7 and 7 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jul'] += item.valor_total
                        valor_mes['jul'] += item.valor_total
                    if item.data_insert.month <= 8 and 8 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['ago'] += item.valor_total
                        valor_mes['ago'] += item.valor_total
                    if item.data_insert.month <= 9 and 9 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['set'] += item.valor_total
                        valor_mes['set'] += item.valor_total
                    if item.data_insert.month <= 10 and 10 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['out'] += item.valor_total
                        valor_mes['out'] += item.valor_total
                    if item.data_insert.month <= 11 and 11 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['nov'] += item.valor_total
                        valor_mes['nov'] += item.valor_total
                    if item.data_insert.month <= 12 and 12 <= datetime.date.today().month:
                        if item.empresa == 'NEAD':
                            valor_mes_nead['dez'] += item.valor_total
                        valor_mes['dez'] += item.valor_total
    
        count = 0
        total = 0
        media = 0
        total_servico = 0
        media_servico = 0
        total_geral = 0
        total_nead = 0

        for key in valor_mes_nead:
            if valor_mes_nead[key] != 0:
                total_nead += valor_mes_nead[key]
            else:
                valor_mes_nead[key] = '-'

        for key in valor_mes_servicos:
            if valor_mes_servicos[key] != 0:
                valor_mes_total[key] += valor_mes_servicos[key]
                count += 1
                total_servico += valor_mes_servicos[key]
            else:
                valor_mes_servicos[key] = '-'
        if count != 0 :      
            media_servico = total_servico/count
        else :
            media_servico = total_servico
        count = 0

        for key in valor_mes:
            if valor_mes[key] != 0:
                valor_mes_total[key] += valor_mes[key]
                count += 1
                total += valor_mes[key]
            else:
                valor_mes[key] = '-'
        
        if count != 0 : 
            media = total/count
        else :
            media = total

        for key in valor_mes_total:
            if valor_mes_total[key] != 0:
                total_geral += valor_mes_total[key]
            else:
                valor_mes_total[key] = '-'

        total_unidades = 0
        for item in Unidades.objects.all() :
            uni.append(unidade(item.sede, item.qtd_user, item.qtd_user/total_user*100, (float)(total_geral - total_nead)*(item.qtd_user/total_user)))
            total_unidades += (float)(total_geral - total_nead)*(item.qtd_user/total_user)

        return render(request, 'hosting/financeiro_senai.html', {'data': data, 'lista_anos': anos, 'valor_mes': valor_mes, 'media': round(media,2), 'previsao': round(media*12,2), 'total': round(total,2), 'mes_atual': datetime.date.today().strftime("%B"), 'valor_mes_servicos': valor_mes_servicos, 'total_servico': round(total_servico,2), 'media_servico': round(media_servico,2), 'previsao_servico': round(media_servico*12,2), 'valor_mes_total': valor_mes_total, 'total_geral': round(total_geral,2), 'valor_mes_nead': valor_mes_nead, 'total_nead': round(total_nead,2), 'unidades': uni, 'total_user': round(total_user,2), 'total_unidades': round(total_unidades, 2)})

    return render(request, 'hosting/financeiro_senai.html')
def get_years():
    anos = []
    for item in Hosting.objects.all():
            if anos.__len__() == 0:
                if(item.data_insert is None):
                    continue
                anos.append(item.data_insert.year)
            if(anos.count(item.data_insert.year) == 0) :
                anos.append(item.data_insert.year)
    
    return anos

def historico(request):
    #colocar todos os meses no contex
    #tentar pegar em qual mes foi clicado no ajax
    #sabendo qual mes foi clicado, reexibir as tabelas para o mes selecionado
    #colocar os 12 meses
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
            if item.hosting_senai & (item.data_delete==date):
                hosting_list.append(item)

        context['mes'] = datetime.date.today().strftime("%B - %Y")
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
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'linux']
    success_url = reverse_lazy('hosting_list')

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(HostingCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo hosting'
        context['maq'] = 'Virtual'
        return context

    def form_valid(self, form):
        if(self.request.POST['ambiente'] == 'fieb'):
            form.instance.hosting_fieb = True
        if(self.request.POST['ambiente'] == 'senai'):
            form.instance.hosting_senai = True
        if 'linux' in self.request.POST:
                    if self.request.POST['linux'] == 'on' :
                        form.instance.islinux = True
        else :
            form.instance.islinux = False
        form.instance.tipo_maq = self.request.POST['maquina']
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
        form.instance.empresa = form.instance.empresa.upper()
        form.instance.tipo_maq = form.instance.tipo_maq.capitalize()
        form.instance.tipo = tipo(form.instance.cpu, form.instance.memoria, form.instance.linux)
        form.instance.recurso = recurso(form.instance.tipo)
        form.instance.perfil = self.request.POST['perfilTeste'].upper()
        form.instance.valor_tabela = valorTabela(form, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = mem_adicional(form.instance.tipo, form.instance.memoria, form.instance.linux)
        form.instance.proc_adicional = cpu_adicional(form.instance.tipo, form.instance.cpu, form.instance.linux)
        form.instance.disco_adicional = disc_adicional(form.instance.disco, form.instance.islinux, form.instance.tipo)
        form.instance.server = form.instance.server.upper()

        if(form.instance.disco_adicional > 0):
            if form.instance.perfil == 'PLATINUM' :
                form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 1.056, 2)
            else:
                form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 0.704, 2)
        else:
            form.instance.valor_disco_adicional = 0
        if(form.instance.memoria_adicional > 0):
            form.instance.valor_memoria_adicional =  round(form.instance.memoria_adicional * 54.904, 2)
        else:
            form.instance.valor_memoria_adicional = 0
        if(form.instance.proc_adicional > 0):
            if form.instance.perfil == 'PLATINUM' :
                form.instance.valor_proc_adicional =  round(form.instance.proc_adicional * 80.2675, 2)
            else:
                form.instance.valor_proc_adicional =  round(form.instance.proc_adicional * 53.512, 2)
        else:
            form.instance.valor_proc_adicional = 0

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingCreate, self).form_valid(form)

def disc_adicional(disco, islinux, tipo):
    if islinux :
        if tipo == 3 :
            return disco - 250
        elif tipo == 2 :
            return disco - 100
        else :
            return disco - 50
    else:
        return disco - 80

def mem_adicional(tipo, mem, islinux):

    if islinux :
        if tipo == 2 :
            return mem - 4
        elif tipo == 3 :
            return mem - 10
        else :
            return mem - 2
    else :
        if(tipo == 2):
            return mem - 8
        elif(tipo == 3):
            return mem - 16
        else:
            return mem - 4

def cpu_adicional(tipo, cpu, islinux):
    if islinux :
        if tipo == 2 :
            return cpu - 2
        elif tipo == 3 :
            return cpu - 4
        else :
            return cpu - 1
    else :
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

def tipo(cpu, mem, islinux):
    tipo_cpu = 1
    tipo_mem = 1
    if islinux :
        if cpu >= 4 :
            tipo_cpu = 3
        elif cpu == 2 :
            tipo_cpu = 2
        else :
            tipo_cpu = 1
        
        if mem >= 10 :
            tipo_mem = 3
        elif mem >=4 :
            tipo_mem = 2
        else :
            tipo_mem = 1

    else :
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
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'linux']
    success_url = reverse_lazy('hosting_list')
    
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(HostingUpdate, self).get_context_data(**kwargs)
        path = context['view'].request.path
        id = path.split('/')
        item = Hosting.objects.get(id = id[2])
        context['titulo'] = 'Edit'
        if(item.hosting_fieb) :
            context['ambiente'] = 'fieb'
        else :
            context['ambiente'] = 'senai'
        context['perfil'] = item.perfil
        context['maq'] = item.tipo_maq.capitalize()
        return context

    def form_valid(self, form):
        if(self.request.POST['ambiente'] == 'fieb'):
            form.instance.hosting_fieb = True
        if(self.request.POST['ambiente'] == 'senai'):
            form.instance.hosting_senai = True
        form.instance.tipo_maq = self.request.POST['maquina']
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
        form.instance.empresa = form.instance.empresa.upper()
        form.instance.tipo_maq = form.instance.tipo_maq.capitalize()
        form.instance.tipo = tipo(form.instance.cpu, form.instance.memoria, form.instance.linux)
        form.instance.recurso = recurso(form.instance.tipo)
        form.instance.perfil = self.request.POST['perfilTeste'].upper()
        form.instance.valor_tabela = valorTabela(form, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = mem_adicional(form.instance.tipo, form.instance.memoria, form.instance.linux)
        form.instance.proc_adicional = cpu_adicional(form.instance.tipo, form.instance.cpu, form.instance.linux)
        form.instance.disco_adicional = disc_adicional(form.instance.disco, form.instance.islinux, form.instance.tipo)
        
        if(form.instance.disco_adicional > 0):
            if form.instance.perfil == 'PLATINUM' :
                form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 1.056, 2)
            else:
                form.instance.valor_disco_adicional = round(form.instance.disco_adicional * 0.704, 2)
        else:
            form.instance.valor_disco_adicional = 0
        if(form.instance.memoria_adicional > 0):
            form.instance.valor_memoria_adicional =  round(form.instance.memoria_adicional * 54.904, 2)
        else:
            form.instance.valor_memoria_adicional = 0
        if(form.instance.proc_adicional > 0):
            if form.instance.perfil == 'PLATINUM' :
                form.instance.valor_proc_adicional =  round(form.instance.proc_adicional * 80.2675, 2)
            else:
                form.instance.valor_proc_adicional =  round(form.instance.proc_adicional * 53.512, 2)
        else:
            form.instance.valor_proc_adicional = 0

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingUpdate, self).form_valid(form)

    def post(self, request, *args, **kwargs): 
        
        path = self.request.path
        id = path.split('/')
        item = Hosting.objects.get(id = id[2])
        
        if('edit' in path) :
            if(item.hosting_fieb) :
                item.data_delete = datetime.date.today()
                new_item = Hosting(empresa=self.request.POST['empresa'], server=self.request.POST['server'], descricao=self.request.POST['descricao'], cpu=self.request.POST['cpu'], memoria=self.request.POST['memoria'], disco=self.request.POST['disco'], tipo_maq=self.request.POST['maquina'].capitalize(), perfil=self.request.POST['perfilTeste'])
                new_item.hosting_fieb = True
               
                if 'linux' in self.request.POST:
                    if self.request.POST['linux'] == 'on' :
                        new_item.linux = True
                new_item.tipo = tipo(int(new_item.cpu), int(new_item.memoria), new_item.linux)
                new_item.recurso = recurso(int(new_item.tipo))
                new_item.data_insert = datetime.date.today()
                new_item.data_delete = datetime.date(year = 2000, month= 1, day = 1)
                new_item.valor_tabela = valorTabela(new_item,new_item.perfil, new_item.recurso)
                new_item.memoria_adicional = mem_adicional(int(new_item.tipo), int(new_item.memoria), new_item.linux)
                new_item.proc_adicional = cpu_adicional(int(new_item.tipo), int(new_item.cpu), new_item.linux)
                new_item.disco_adicional = disc_adicional(int(new_item.disco), new_item.linux, new_item.tipo)

                if(new_item.disco_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 1.056, 2)
                    else:
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 0.704, 2)
                else:
                    new_item.valor_disco_adicional = 0
                if(new_item.memoria_adicional > 0):
                    new_item.valor_memoria_adicional =  round(new_item.memoria_adicional * 54.904, 2)
                else:
                    new_item.valor_memoria_adicional = 0
                if(new_item.proc_adicional > 0):
                    print(new_item.recurso)
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 80.2675, 2)
                    else:
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 53.512, 2)
                else:
                    new_item.valor_proc_adicional = 0

                new_item.valor_total = new_item.valor_tabela+new_item.valor_disco_adicional+new_item.valor_memoria_adicional+new_item.valor_proc_adicional
                new_item.save()
                item.save()
                return HttpResponseRedirect(reverse_lazy('hosting_fieb'))
            else :
                print(self.request.POST['maquina'])
                item.data_delete = datetime.date.today()
                new_item = Hosting(empresa=self.request.POST['empresa'], server=self.request.POST['server'], descricao=self.request.POST['descricao'], cpu=self.request.POST['cpu'], memoria=self.request.POST['memoria'], disco=self.request.POST['disco'], tipo_maq=self.request.POST['maquina'].capitalize(), perfil=self.request.POST['perfilTeste'])
                new_item.hosting_senai = True
                
                if 'linux' in self.request.POST:
                    if self.request.POST['linux'] == 'on' :
                        new_item.linux = True
                        
                new_item.tipo = tipo(int(new_item.cpu), int(new_item.memoria), new_item.linux)
                new_item.recurso = recurso(int(new_item.tipo))
                new_item.data_insert = datetime.date.today()
                new_item.data_delete = datetime.date(year = 2000, month= 1, day = 1)
                new_item.valor_tabela = valorTabela(new_item,new_item.perfil, new_item.recurso)
                new_item.memoria_adicional = mem_adicional(int(new_item.tipo), int(new_item.memoria), new_item.linux)
                new_item.proc_adicional = cpu_adicional(int(new_item.tipo), int(new_item.cpu), new_item.linux)
                new_item.disco_adicional = disc_adicional(int(new_item.disco), new_item.linux, new_item.tipo)

                if(new_item.disco_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 1.056, 2)
                    else:
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 0.704, 2)
                else:
                    new_item.valor_disco_adicional = 0
                if(new_item.memoria_adicional > 0):
                    new_item.valor_memoria_adicional =  round(new_item.memoria_adicional * 54.904, 2)
                else:
                    new_item.valor_memoria_adicional = 0
                if(new_item.proc_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 80.2675, 2)
                    else :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 53.512, 2)
                else:
                    new_item.valor_proc_adicional = 0

                new_item.valor_total = new_item.valor_tabela+new_item.valor_disco_adicional+new_item.valor_memoria_adicional+new_item.valor_proc_adicional
                new_item.save()
                item.save()
                return HttpResponseRedirect(self.success_url)
                
        else:
            if(item.hosting_fieb) :
                item.data_delete = datetime.date.today()
                new_item = Hosting(empresa=self.request.POST['empresa'], server=self.request.POST['server'], descricao=self.request.POST['descricao'], cpu=self.request.POST['cpu'], memoria=self.request.POST['memoria'], disco=self.request.POST['disco'], tipo_maq=self.request.POST['maquina'].capitalize(), perfil=self.request.POST['perfilTeste'])
                new_item.hosting_fieb = True
               
                if 'linux' in self.request.POST:
                    if self.request.POST['linux'] == 'on' :
                        new_item.linux = True
                new_item.tipo = tipo(int(new_item.cpu), int(new_item.memoria), new_item.linux)
                new_item.recurso = recurso(int(new_item.tipo))
                new_item.data_insert = datetime.date.today()
                new_item.data_delete = datetime.date(year = 2000, month= 1, day = 1)
                new_item.valor_tabela = valorTabela(new_item,new_item.perfil, new_item.recurso)
                new_item.memoria_adicional = mem_adicional(int(new_item.tipo), int(new_item.memoria), new_item.linux)
                new_item.proc_adicional = cpu_adicional(int(new_item.tipo), int(new_item.cpu), new_item.linux)
                new_item.disco_adicional = disc_adicional(int(new_item.disco), new_item.linux, new_item.tipo)

                if(new_item.disco_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 1.056, 2)
                    else:
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 0.704, 2)
                else:
                    new_item.valor_disco_adicional = 0
                if(new_item.memoria_adicional > 0):
                    new_item.valor_memoria_adicional =  round(new_item.memoria_adicional * 54.904, 2)
                else:
                    new_item.valor_memoria_adicional = 0
                if(new_item.proc_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 80.2675, 2)
                    else :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 53.512, 2)
                else:
                    new_item.valor_proc_adicional = 0

                new_item.valor_total = new_item.valor_tabela+new_item.valor_disco_adicional+new_item.valor_memoria_adicional+new_item.valor_proc_adicional
                new_item.save()
                item.save()
                return HttpResponseRedirect(reverse_lazy('hosting_fieb'))
            else :
                item.data_delete = datetime.date.today()
                new_item = Hosting(empresa=self.request.POST['empresa'], server=self.request.POST['server'], descricao=self.request.POST['descricao'], cpu=self.request.POST['cpu'], memoria=self.request.POST['memoria'], disco=self.request.POST['disco'], tipo_maq=self.request.POST['maquina'].capitalize(), perfil=self.request.POST['perfilTeste'])
                new_item.hosting_senai = True
                
                if 'linux' in self.request.POST:
                    if self.request.POST['linux'] == 'on' :
                        new_item.linux = True
                new_item.tipo = tipo(int(new_item.cpu), int(new_item.memoria), new_item.linux)
                new_item.recurso = recurso(int(new_item.tipo))
                new_item.data_insert = datetime.date.today()
                new_item.data_delete = datetime.date(year = 2000, month= 1, day = 1)
                new_item.valor_tabela = valorTabela(new_item,new_item.perfil, new_item.recurso)
                new_item.memoria_adicional = mem_adicional(int(new_item.tipo), int(new_item.memoria), new_item.linux)
                new_item.proc_adicional = cpu_adicional(int(new_item.tipo), int(new_item.cpu), new_item.linux)
                new_item.disco_adicional = disc_adicional(int(new_item.disco), new_item.linux, new_item.tipo)

                if(new_item.disco_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 1.056, 2)
                    else:
                        new_item.valor_disco_adicional = round(new_item.disco_adicional * 0.704, 2)
                else:
                    new_item.valor_disco_adicional = 0
                if(new_item.memoria_adicional > 0):
                    new_item.valor_memoria_adicional =  round(new_item.memoria_adicional * 54.904, 2)
                else:
                    new_item.valor_memoria_adicional = 0
                if(new_item.proc_adicional > 0):
                    if new_item.perfil == 'PLATINUM' :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 80.2675, 2)
                    else :
                        new_item.valor_proc_adicional =  round(new_item.proc_adicional * 53.512, 2)
                else:
                    new_item.valor_proc_adicional = 0

                new_item.valor_total = new_item.valor_tabela+new_item.valor_disco_adicional+new_item.valor_memoria_adicional+new_item.valor_proc_adicional
                new_item.save()
                item.save()
                return HttpResponseRedirect(self.success_url)
        
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
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(self.success_url)
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)

class Sevicos_adicionaisCreate (CreateView):
    model = Servicos_adicionais
    fields = ['descricao', 'ticket','duracao', 'observacao', 'responsavel', 'valor']
    success_url = reverse_lazy('servicos')
    
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(Sevicos_adicionaisCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo Serviço'
        context['home'] = 'senai'
        return context

    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)

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
    fields = ['descricao', 'valorUnitario','volume', 'quantidade']
    success_url = reverse_lazy('servicos')

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(Backup_dadosCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo Backup'
        context['home'] = 'senai'
        return context

    def form_valid(self, form):
        form.instance.casa = form.instance.casa.upper()
        if(form.instance.quantidade == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.volume
        if(form.instance.volume == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.quantidade

        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
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

class unidade:
    def __init__(self, unidade, qtd, porcentagem, valor):
        self.unidade = unidade
        self.qtd = qtd
        self.porcentagem = round(porcentagem, 2)
        self.valor = round(valor,2)
