from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hosting, Servicos_adicionais, Backup_dados, Unidades
from .helper import Auxiliares
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
import datetime
from django.core import serializers
from django.http import HttpResponseRedirect

class Paginas:
    @staticmethod
    def tabelaPrecos(request):
        """
            Método que gerencia a página de tabela de preços. 
            Recebe como parâmetro 'request' da pagina que possue GET e POST da página.
        """
        data_inteira = Auxiliares.mes_atual(datetime.date.today())
        data = data_inteira.strftime("%B - %Y")
        teste = 'Recurso'
        return render(request, 'hosting/tabela_preco.html', {'data': data, 'teste': teste})
    @staticmethod
    def add_client(request):
        """
            Método que gerencia a página de inserção de clientes para escolha de hosting, serviço adicional ou backup.
            Recebe como parâmetro 'request' da pagina que possue GET e POST da página.
        """
        return render(request, 'hosting/add_client.html')
    @staticmethod
    def hostingFieb(request):
        """
            Método que gerencia a página que apresenta os hostings do ambiente fieb.
            Recebe como parâmetro 'request' da pagina que possue GET e POST da página.
        """
        data = datetime.date.today().strftime("%B - %Y")
        hosting_list = []
        hosting_list_search = []
        date = datetime.date(year = 2000, month= 1, day = 1)
        total= 0
        list_dic = []
        ordena = None
        mes_selecionado = datetime.date.today().strftime('%B - %Y')
        mes_atual = datetime.date.today().strftime('%B - %Y')

        if datetime.date.today().month != 1 and datetime.date.today().month != 2:
            mes_anterior = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 1, day = datetime.date.today().day).strftime('%B - %Y')
            mes_anterior2 = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 2, day = datetime.date.today().day).strftime('%B - %Y')

        elif datetime.date.today().month == 1:
            mes_anterior = datetime.date(year = datetime.date.today().year - 1, month= 12 , day = datetime.date.today().day).strftime('%B - %Y')
            mes_anterior2 = datetime.date(year = datetime.date.today().year - 1, month= 11 - 2, day = datetime.date.today().day).strftime('%B - %Y')

        else:
            mes_anterior = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 1, day = datetime.date.today().day).strftime('%B - %Y')
            mes_anterior2 = datetime.date(year = datetime.date.today().year, month= 12, day = datetime.date.today().day).strftime('%B - %Y')

        if 'meses' in request.GET :
            hosting_list_search = list(Hosting.objects.filter(hosting_fieb=True))
            mes_selecionado = request.GET['meses']
            mes = request.GET['meses'].split('-')
            hosting_list = Auxiliares.search(mes[0].strip(), mes[1].strip(), hosting_list_search)
        else:
            hosting_list = list(Hosting.objects.filter(hosting_fieb=True, data_delete=date))

        if 'search' in request.GET and request.GET['search'] != '':
        
            for item in hosting_list:  
                if (request.GET['search'].upper() in item.empresa or request.GET['search'].upper() in item.server or request.GET['search'] in item.descricao or request.GET['search'].capitalize() in item.descricao or request.GET['search'].upper() in item.descricao or request.GET['search'].capitalize() in item.descricao.capitalize()):
                    hosting_list_search.append(item)

            if 'ordem' in request.GET :
                ordena = request.GET['ordem']
                hosting_list_search = Auxiliares.ordenar(ordena, hosting_list_search)

            for item in hosting_list :
                    total += item.valor_total

            return render(request, 'hosting/hosting_fieb.html', {'mes': data, 'total': total, 'totalAno': total*12,'total_empresa': list_dic, 'hosting_list': hosting_list_search, 'tabela': 'SENAI', 'pesquisa':request.GET['search'], 'ordena': ordena, 'mes_atual': mes_atual, 'mes_selecionado': mes_selecionado, 'mes_selecionado': mes_selecionado, 'mes_atual': mes_atual, 'mes_anterior': mes_anterior, 'mes_anterior2': mes_anterior2})
        else :
            if 'ordem' in request.GET :
                ordena = request.GET['ordem']
                hosting_list = Auxiliares.ordenar(ordena, hosting_list)

            list_dic = Auxiliares.empresas(hosting_list)

            for item in hosting_list :
                total = item.valor_total + total

            return render(request, 'hosting/hosting_fieb.html', {'mes': data, 'total': total, 'totalAno': total*12,'total_empresa': list_dic, 'hosting_list': hosting_list, 'tabela': 'SENAI', 'ordena': ordena, 'mes_selecionado': mes_selecionado, 'mes_atual': mes_atual, 'mes_anterior': mes_anterior, 'mes_anterior2': mes_anterior2, 'mes_atual': mes_atual, 'mes_selecionado': mes_selecionado})
    @staticmethod
    def servicos_adicionais(request):
        """
            Método que gerencia a página que apresenta os serviços adicionais e backups.
            Recebe como parâmetro 'request' da pagina que possue GET e POST da página.
        """
        data = datetime.date.today().strftime("%B - %Y")
        servico_list = []
        backup_list = []
        date = datetime.date(year = 2000, month= 1, day = 1)
        ambiente = 'senai'

        if 'ambiente' in request.GET:
            if request.GET['ambiente'] == 'senai':
                for item in list(Servicos_adicionais.objects.filter(ambiente='senai', data_delete=date)):
                    servico_list.append(item)

                for item in list(Backup_dados.objects.filter(ambiente='senai', data_delete=date)):
                    backup_list.append(item)
            elif request.GET['ambiente'] == 'fieb':
                ambiente = 'fieb'
                for item in list(Servicos_adicionais.objects.filter(ambiente='fieb', data_delete=date)):
                    servico_list.append(item)

                for item in list(Backup_dados.objects.filter(ambiente='fieb', data_delete=date)):
                    backup_list.append(item)
        else:
            for item in list(Servicos_adicionais.objects.filter(ambiente='senai', data_delete=date)):
                servico_list.append(item)

            for item in list(Backup_dados.objects.filter(ambiente='senai', data_delete=date)):
                backup_list.append(item)

        totais = Auxiliares.somar_servicos(servico_list, backup_list)

        return render(request, 'hosting/servicos.html', {'mes': data, 'total_servico': totais['servico'], 'total_backup': totais['backup'], 'total_adicionais': totais['total'], 'casa_senai': totais['senai'], 'casa_sesi': totais['sesi'], 'casa_fieb': totais['fieb'], 'casa_iel': totais['iel'], 'backup_list': backup_list, 'servico_list': servico_list, 'ambiente': ambiente})
    @staticmethod
    def redirectSenai(request):
        """
            Realiza o redicerionamento para HostingList (página inicial).
        """
        return redirect('hosting_list')
    @staticmethod
    def financeiroSENAI(request):
        """
            Método que gerencia a página do financeiro. 
            Recebe como parâmetro 'request' da pagina que possue GET e POST da página.
        """
        data_inteira = Auxiliares.mes_atual(datetime.date.today())
        data = data_inteira.strftime("%B - %Y")
        valor_mes = Auxiliares.dic_meses()
        valor_mes_nead = Auxiliares.dic_meses()
        valor_mes_servicos = Auxiliares.dic_meses()
        valor_mes_total = Auxiliares.dic_meses()
        anos = Auxiliares.get_years()
        total_user = 0
        count = 0
        uni = []
        qtd_unidades = []
        backup_list_senai = list(Backup_dados.objects.filter(ambiente='senai'))
        servico_list_senai = list(Servicos_adicionais.objects.filter(ambiente='senai'))
        hosting_list_senai = list(Hosting.objects.filter(hosting_senai='True'))

        backup_list_fieb = list(Backup_dados.objects.filter(ambiente='fieb'))
        servico_list_fieb = list(Servicos_adicionais.objects.filter(ambiente='fieb'))
        hosting_list_fieb = list(Hosting.objects.filter(hosting_fieb='True'))
        
        if not anos:
            anos.append(2019)
        if 'quantidade' in request.POST:
            qtd_unidades = dict(request.POST)['quantidade']
            for item in Unidades.objects.all() :
                if qtd_unidades:
                    item.qtd_user = int(qtd_unidades[count])
                    item.save()
                    count+=1
        for item in Unidades.objects.all() :
                total_user += item.qtd_user
        if request.GET:
            if request.GET['ambiente'] == 'senai':
                mes_f = datetime.date(year = 2000, month= int(request.GET['mesF']), day = 1).strftime("%B")
                mes_i = datetime.date(year = 2000, month= int(request.GET['mesI']), day = 1).strftime("%B")
                
                    
                valor_mes_servicos, valor_mes_servicosFSI = Auxiliares.somar_servicos(servico_list_senai,backup_list_senai, tipo='pesquisa', inicial=request.GET['mesI'], final=request.GET['mesF'], ano=request.GET['ano'])
                valor_mes, valor_mes_nead = Auxiliares.valor_mes_nead_senai(hosting_list_senai, tipo='pesquisa', inicial=request.GET['mesI'], final=request.GET['mesF'], ano=request.GET['ano'])
                valor_mes_total = Auxiliares.somar_total(valor_mes_nead, valor_mes, valor_mes_servicos, valor_mes_servicosFSI, soma_dic=True)
                total_nead = Auxiliares.somar_total(valor_mes_nead)
                total_geral = Auxiliares.somar_total(valor_mes_total)
                total_servicoFSI = Auxiliares.somar_total(valor_mes_servicosFSI)
                total_servico = Auxiliares.somar_total(valor_mes_servicos)
                total = Auxiliares.somar_total(valor_mes)

                media_servicoFSI = Auxiliares.valor_medio(valor_mes_servicosFSI)
                media_servico = Auxiliares.valor_medio(valor_mes_servicos)
                media = Auxiliares.valor_medio(valor_mes)

                total_unidades = 0
                for item in Unidades.objects.all() :
                    uni.append(Unidade(item.sede, item.qtd_user, item.qtd_user/total_user*100, (float)(total_geral - total_nead)*(item.qtd_user/total_user)))
                    total_unidades += (float)(total_geral - total_nead)*(item.qtd_user/total_user)

                return render(request, 'hosting/financeiro_senai.html', {'data': data, 'lista_anos': anos, 'valor_mes': valor_mes, 'media': round(media,2), 'previsao': round(media*12,2), 'total': round(total,2), 'mes_atual': mes_f, 'valor_mes_servicos': valor_mes_servicos, 'total_servico': round(total_servico,2), 'media_servico': round(media_servico,2), 'previsao_servico': round(media_servico*12,2), 'valor_mes_total': valor_mes_total, 'total_geral': round(total_geral,2), 'valor_mes_nead': valor_mes_nead, 'total_nead': round(total_nead,2), 'unidades': uni, 'total_user': round(total_user,2), 'total_unidades': round(total_unidades, 2), 'mes_i': mes_i, 'ambiente': 'senai', 'valor_mes_servicosFSI': valor_mes_servicosFSI, 'media_servicoFSI': media_servicoFSI, 'total_servicoFSI': total_servicoFSI, 'previsao_servicoFSI': round(media_servicoFSI*12,2)})
            else: 
                mes_f = datetime.date(year = 2000, month= int(request.GET['mesF']), day = 1).strftime("%B")
                mes_i = datetime.date(year = 2000, month= int(request.GET['mesI']), day = 1).strftime("%B")
                    
                valor_mes_servicos, valor_mes_servicosFSI = Auxiliares.somar_servicos(servico_list_fieb,backup_list_fieb, tipo='pesquisa', inicial=request.GET['mesI'], final=request.GET['mesF'], ano=request.GET['ano'])
                valor_mes_total, valor_mes_fieb, valor_mes_gti, valor_mes_iel, valor_mes_sesi = Auxiliares.valor_mes_nead_senai(hosting_list_fieb, tipo='pesquisa', inicial=request.GET['mesI'], final=request.GET['mesF'], ano=request.GET['ano'], ambiente='fieb')

                valor_mes_total = Auxiliares.somar_total(valor_mes_total, valor_mes_servicosFSI, valor_mes_servicos, soma_dic=True)
                total_servicoFSI = Auxiliares.somar_total(valor_mes_servicosFSI)
                total = Auxiliares.somar_total(valor_mes_gti)
                total_servico = Auxiliares.somar_total(valor_mes_servicos)
                total_fieb = Auxiliares.somar_total(valor_mes_fieb)
                total_sesi = Auxiliares.somar_total(valor_mes_sesi)
                total_iel = Auxiliares.somar_total(valor_mes_iel)
                total_geral = Auxiliares.somar_total(valor_mes_total)
                media_servico = Auxiliares.somar_total(valor_mes_servicos)
                media_servicoFSI = Auxiliares.valor_medio(valor_mes_servicosFSI)
                media = Auxiliares.valor_medio(valor_mes_gti)
                media_fieb = Auxiliares.valor_medio(valor_mes_fieb)
                media_sesi = Auxiliares.valor_medio(valor_mes_sesi)
                media_iel = Auxiliares.valor_medio(valor_mes_iel)


                return render(request, 'hosting/financeiro_senai.html', {'data': data, 'lista_anos': anos, 'valor_mes': valor_mes_gti, 'media': round(media,2), 'previsao': round(media*12,2), 'total': round(total,2), 'mes_atual': mes_f, 'valor_mes_total': valor_mes_total, 'total_geral': round(total_geral,2), 'mes_i': mes_i, 'ambiente': request.GET['ambiente'], 'valor_fieb': valor_mes_fieb, 'media_fieb': round(media_fieb,2), 'previsao_fieb': round(media_fieb*12,2), 'total_fieb': round(total_fieb,2), 'media_sesi': round(media_sesi,2), 'previsao_sesi': round(media_sesi*12,2), 'total_sesi': round(total_sesi,2), 'media_iel': round(media_iel, 2), 'previsao_iel': round(media_iel*12,2), 'total_iel': round(total_iel,2), 'valor_sesi': valor_mes_sesi, 'valor_iel': valor_mes_iel, 'valor_mes_servicosFSI': valor_mes_servicosFSI, 'media_servicoFSI': round(media_servicoFSI,2), 'total_servicoFSI': round(total_servicoFSI,2), 'previsao_servicoFSI': round(media_servicoFSI*12,2), 'valor_mes_servicos': valor_mes_servicos, 'total_servico': round(total_servico,2), 'media_servico': round(media_servico,2), 'previsao_servico': round(media_servico*12,2)})
        else:
            valor_mes_servicos, valor_mes_servicosFSI = Auxiliares.somar_servicos(servico_list_senai,backup_list_senai, tipo='mes')
            valor_mes, valor_mes_nead = Auxiliares.valor_mes_nead_senai(hosting_list_senai)
            valor_mes_total = Auxiliares.somar_total(valor_mes_nead, valor_mes, valor_mes_servicos, valor_mes_servicosFSI, soma_dic=True)
            total_nead = Auxiliares.somar_total(valor_mes_nead)
            total_geral = Auxiliares.somar_total(valor_mes_total)
            total_servicoFSI = Auxiliares.somar_total(valor_mes_servicosFSI)
            total_servico = Auxiliares.somar_total(valor_mes_servicos)
            total = Auxiliares.somar_total(valor_mes)

            media_servicoFSI = Auxiliares.valor_medio(valor_mes_servicosFSI)
            media_servico = Auxiliares.valor_medio(valor_mes_servicos)
            media = Auxiliares.valor_medio(valor_mes)

            total_unidades = 0
            
            for item in Unidades.objects.all() :
                uni.append(Unidade(item.sede, item.qtd_user, item.qtd_user/total_user*100, (float)(total_geral - total_nead)*(item.qtd_user/total_user)))
                total_unidades += (float)(total_geral - total_nead)*(item.qtd_user/total_user)

            return render(request, 'hosting/financeiro_senai.html', {'data': data, 'lista_anos': anos, 'valor_mes': valor_mes, 'media': round(media,2), 'previsao': round(media*12,2), 'total': round(total,2), 'mes_atual': data_inteira.strftime('%B'), 'valor_mes_servicos': valor_mes_servicos, 'total_servico': round(total_servico,2), 'media_servico': round(media_servico,2), 'previsao_servico': round(media_servico*12,2), 'valor_mes_total': valor_mes_total, 'total_geral': round(total_geral,2), 'valor_mes_nead': valor_mes_nead, 'total_nead': round(total_nead,2), 'unidades': uni, 'total_user': round(total_user,2), 'total_unidades': round(total_unidades, 2), 'mes_i': 'January', 'ambiente': 'senai', 'valor_mes_servicosFSI': valor_mes_servicosFSI, 'media_servicoFSI': media_servicoFSI, 'total_servicoFSI': total_servicoFSI, 'previsao_servicoFSI': round(media_servicoFSI*12,2)})

class HostingList(ListView):
    """
        Classe que herda de ListView para implementar seus métodos no genrenciamento da página de exibição de hostings do ambiente SENAI.
        Utilizado para dizer o model (atributos que estão no banco) que será utilizado para ser exibido na página.
    """
    model = Hosting

    def get_context_data(self, **kwargs):
        """
            Método que é executado quando a página é chamada.
        """
        context = super(HostingList, self).get_context_data(**kwargs)
 
        hosting_list = []
        hosting_search = []
        date = datetime.date(year = 2000, month= 1, day = 1)
        context['mes'] = datetime.date.today().strftime("%B - %Y")
        context['mes_selecionado'] = datetime.date.today().strftime('%B - %Y')
        context['mes_atual'] = datetime.date.today().strftime('%B - %Y')
        
        if datetime.date.today().month != 1 and datetime.date.today().month != 2:
            context['mes_anterior'] = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 1, day = datetime.date.today().day).strftime('%B - %Y')
            context['mes_anterior2'] = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 2, day = datetime.date.today().day).strftime('%B - %Y')

        elif datetime.date.today().month == 1:
            context['mes_anterior'] = datetime.date(year = datetime.date.today().year - 1, month= 12 , day = datetime.date.today().day).strftime('%B - %Y')
            context['mes_anterior2'] = datetime.date(year = datetime.date.today().year - 1, month= 11 - 2, day = datetime.date.today().day).strftime('%B - %Y')

        else:
            context['mes_anterior'] = datetime.date(year = datetime.date.today().year, month= datetime.date.today().month - 1, day = datetime.date.today().day).strftime('%B - %Y')
            context['mes_anterior2'] = datetime.date(year = datetime.date.today().year, month= 12, day = datetime.date.today().day).strftime('%B - %Y')
        
        total= 0
        list_dic = []

        if 'meses' in self.request.GET :
            hosting_search = list(Hosting.objects.filter(hosting_senai=True))
            context['mes_selecionado'] = self.request.GET['meses']
            mes = self.request.GET['meses'].split('-')
            hosting_list = Auxiliares.search(mes[0].strip(), mes[1].strip(), hosting_search)
            context['hosting_list'] = hosting_list 
        else:
            hosting_list = list(Hosting.objects.filter(hosting_senai=True, data_delete=date))        
        
        if 'search' in self.request.GET and self.request.GET['search'] != '' :
            for item in hosting_list:
                if self.request.GET['search'].upper() in item.empresa or self.request.GET['search'].upper() in item.server or self.request.GET['search'] in item.descricao or self.request.GET['search'].capitalize() in item.descricao or self.request.GET['search'].upper() in item.descricao or self.request.GET['search'].capitalize() in item.descricao.capitalize():
                    hosting_search.append(item)

            if 'ordem' in self.request.GET :
                context['ordena'] = self.request.GET['ordem']
                hosting_search = Auxiliares.ordenar(context['ordena'], hosting_search)        

            context['hosting_list'] = hosting_search
            for item in context['hosting_list'] :
                total += item.valor_total

            context['total'] = total
            context['pesquisa'] = self.request.GET['search']
        else:
            if 'ordem' in self.request.GET :
                context['ordena'] = self.request.GET['ordem']
                hosting_search = Auxiliares.ordenar(context['ordena'], hosting_search) 
                context['hosting_list'] = hosting_search   
            else:
                context['hosting_list'] = hosting_list
            list_dic = Auxiliares.empresas(hosting_list)

            for item in context['hosting_list'] :
                total = item.valor_total + total

            context['total'] = total
            context['totalAno'] = total*12
            context['total_empresa'] = list_dic
            context['tabela'] = 'SENAI'
            
        return context

class HostingCreate(CreateView):
    """
        Classe que herda de CreateView para implementar seus métodos no genrenciamento da página de criação de hosting.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de inserção, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Hosting
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'linux']
    success_url = reverse_lazy('hosting_list')

    def get_context_data(self, **kwargs):
        """
            Método que é executado quando a página é chamada.
            Pode ser utilizado para passa variáveis.
        """
        context = super(HostingCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo hosting'
        context['maq'] = 'Virtual'
        return context

    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para adição.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        if self.request.POST['ambiente'] == 'fieb' :
            form.instance.hosting_fieb = True
            self.success_url = reverse_lazy('hosting_fieb')
        elif self.request.POST['ambiente'] == 'senai' :
            form.instance.hosting_senai = True
        else:
            pass
    
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
        form.instance.tipo = Auxiliares.tipo(form.instance.cpu, form.instance.memoria, form.instance.linux)
        form.instance.recurso = Auxiliares.recurso(form.instance.tipo)
        form.instance.perfil = self.request.POST['perfil'].upper()
        form.instance.valor_tabela = Auxiliares.valor_tabela(form.instance.tipo_maq, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = Auxiliares.mem_adicional(form.instance.tipo, form.instance.memoria, form.instance.linux)
        form.instance.proc_adicional = Auxiliares.cpu_adicional(form.instance.tipo, form.instance.cpu, form.instance.linux)
        form.instance.disco_adicional = Auxiliares.disc_adicional(form.instance.disco, form.instance.islinux, form.instance.tipo)
        form.instance.server = form.instance.server.upper()

        form.instance.valor_disco_adicional = Auxiliares.valor_disco_adicional(form.instance.disco_adicional, form.instance.perfil)
        form.instance.valor_memoria_adicional = Auxiliares.valor_mem_adicional(form.instance.memoria_adicional)
        form.instance.valor_proc_adicional = Auxiliares.valor_proc_adicional(form.instance.proc_adicional, form.instance.perfil)

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingCreate, self).form_valid(form)

class HostingUpdate(UpdateView):
    """
        Classe que herda de CreateView para implementar seus métodos no genrenciamento da página de criação de hosting.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de atualização, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Hosting
    fields = ['empresa', 'server','descricao', 'cpu', 'memoria', 'disco', 'linux']
    success_url = reverse_lazy('hosting_list')
    
    def get_context_data(self, **kwargs):
        """
            Método que é executado ao carregar a página de atualização.
            Pode ser utilizado para passar informações do item que será alterado.
        """
        context = super(HostingUpdate, self).get_context_data(**kwargs)
        path = context['view'].request.path
        id = path.split('/')
        item = Hosting.objects.get(id = id[2])
        context['titulo'] = 'Editar hosting'
        if(item.hosting_fieb) :
            context['ambiente'] = 'fieb'
        else :
            context['ambiente'] = 'senai'
        context['perfil'] = item.perfil
        context['maq'] = item.tipo_maq.capitalize()
        return context

    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para adição.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        if(self.request.POST['ambiente'] == 'fieb'):
            form.instance.hosting_fieb = True
        if(self.request.POST['ambiente'] == 'senai'):
            form.instance.hosting_senai = True
        form.instance.tipo_maq = self.request.POST['maquina']
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
        form.instance.empresa = form.instance.empresa.upper()
        form.instance.tipo_maq = form.instance.tipo_maq.capitalize()
        form.instance.tipo = Auxiliares.tipo(form.instance.cpu, form.instance.memoria, form.instance.linux)
        form.instance.recurso = Auxiliares.recurso(form.instance.tipo)
        form.instance.perfil = self.request.POST['perfil'].upper()
        form.instance.valor_tabela = Auxiliares.valor_tabela(form.instance.tipo_maq, form.instance.perfil, form.instance.recurso)
        form.instance.memoria_adicional = Auxiliares.mem_adicional(form.instance.tipo, form.instance.memoria, form.instance.linux)
        form.instance.proc_adicional = Auxiliares.cpu_adicional(form.instance.tipo, form.instance.cpu, form.instance.linux)
        form.instance.disco_adicional = Auxiliares.disc_adicional(form.instance.disco, form.instance.islinux, form.instance.tipo)
        
        form.instance.valor_disco_adicional = Auxiliares.valor_disco_adicional(form.instance.disco_adicional, form.instance.perfil)
        form.instance.valor_memoria_adicional = Auxiliares.valor_mem_adicional(form.instance.memoria_adicional)
        form.instance.valor_proc_adicional = Auxiliares.valor_proc_adicional(form.instance.proc_adicional, form.instance.perfil)

        form.instance.valor_total = form.instance.valor_tabela+form.instance.valor_disco_adicional+form.instance.valor_memoria_adicional+form.instance.valor_proc_adicional
        return super(HostingUpdate, self).form_valid(form)

    def post(self, request, *args, **kwargs): 
        """
            Método invocado quando é submetido o formulário para edição do hosting.
            O item não será excluido do banco, o campo data_delete receberá a data do dia e será criado um novo item com os novos valores.
        """
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
                new_item.valor_tabela = valorTabela(new_item.tipo_maq,new_item.perfil, new_item.recurso)
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
                    else:
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
                new_item.valor_tabela = valorTabela(new_item.tipo_maq,new_item.perfil, new_item.recurso)
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
                new_item.valor_tabela = valorTabela(new_item.tipo_maq,new_item.perfil, new_item.recurso)
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
                new_item.valor_tabela = valorTabela(new_item.tipo_maq,new_item.perfil, new_item.recurso)
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
    """
        Classe que herda de DeleteView para implementar seus métodos no genrenciamento da página exclusão de hosting.
        Utilizado para dizer o model (atributos  que serão excluidos no banco) que será utilizado, página que deve ser direcionada após a exclusõ bem sucedida e outros campos.
    """
    model = Hosting
    success_url = reverse_lazy('hosting_list')
    
    def post(self, request, *args, **kwargs): 
        """
            Método invocado quando é submetido o formulário para exclusão do hosting.
            O item não será excluido do banco, o campo data_delete receberá a data do dia.
        """
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
    """
        Classe que herda de CreateView para implementar seus métodos no genrenciamento da página de criação de servições adicionais.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de inserção, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Servicos_adicionais
    fields = ['descricao', 'ticket','duracao', 'observacao', 'responsavel', 'valor']
    success_url = reverse_lazy('servicos')
    
    def get_context_data(self, **kwargs):
        """
            Método que é executado quando a página é chamada.
            Pode ser utilizado para passa variáveis.
        """
        context = super(Sevicos_adicionaisCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo serviço'
        context['home'] = 'senai'
        context['ambiente'] = 'senai'
        return context

    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para adição.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        form.instance.casa = str(self.request.POST['casa']).upper()
        form.instance.ambiente = self.request.POST['ambiente']
        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)

        return super(Sevicos_adicionaisCreate, self).form_valid(form)

class Servicos_adicionaisUpdate(UpdateView):
    """
        Classe que herda de UpdateView para implementar seus métodos no genrenciamento da página de edição de servições adicionais.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de atualização, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Servicos_adicionais
    fields = ['descricao', 'ticket','duracao', 'observacao', 'responsavel', 'valor']
    success_url = reverse_lazy('servicos')
    
    def get_context_data(self, **kwargs):
        """
            Método que é executado ao carregar a página de atualização.
            Pode ser utilizado para passar informações do item que será alterado.
        """
        context = super(Servicos_adicionaisUpdate, self).get_context_data(**kwargs)
        path = context['view'].request.path
        id = path.split('/')
        item = Servicos_adicionais.objects.get(id = id[3])
        context['home'] = item.casa
        context['titulo'] = 'Editar Serviço'
        context['ambiente'] = item.ambiente
        return context
    
    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para atualização.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        form.instance.casa = form.instance.casa.upper()
        return super(Servicos_adicionaisUpdate, self).form_valid(form)

class Servicos_adicionaisDelete(DeleteView):
    """
        Classe que herda de DeleteView para implementar seus métodos no genrenciamento da página de exclusão de servições adicionais.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Servicos_adicionais
    success_url = reverse_lazy('servicos')

class Backup_dadosCreate(CreateView):
    """
        Classe que herda de CreateView para implementar seus métodos no genrenciamento da página de criação de backups.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de inserção, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Backup_dados
    fields = ['descricao', 'valorUnitario','volume', 'quantidade']
    success_url = reverse_lazy('servicos')

    def get_context_data(self, **kwargs):
        """
            Método que é executado quando a página é chamada.
            Pode ser utilizado para passa variáveis.
        """
        context = super(Backup_dadosCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo backup'
        context['home'] = 'senai'
        context['ambiente'] = 'senai'
        return context

    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para adição.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        form.instance.casa = str(self.request.POST['casa']).upper()
        form.instance.ambiente = self.request.POST['ambiente']
        if(form.instance.quantidade == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.volume
        if(form.instance.volume == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.quantidade

        form.instance.data_insert = datetime.date.today()
        form.instance.data_delete = datetime.date(year = 2000, month= 1, day = 1)
        return super(Backup_dadosCreate, self).form_valid(form)

class Backup_dadosUpdate(UpdateView):
    """
        Classe que herda de UpdateView para implementar seus métodos no genrenciamento da página de edição de backups.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, informar os campos - fields - que deverão ser exibidos no formulário de atualização, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Backup_dados
    fields = ['descricao', 'valorUnitario','volume', 'quantidade']
    success_url = reverse_lazy('servicos')

    def get_context_data(self, **kwargs):
        """
            Método que é executado ao carregar a página de atualização.
            Pode ser utilizado para passar informações do item que será alterado.
        """
        context = super(Backup_dadosUpdate, self).get_context_data(**kwargs)
        path = context['view'].request.path
        id = path.split('/')
        item = Backup_dados.objects.get(id = id[3])
        context['home'] = str(item.casa).lower()
        context['titulo'] = 'Editar Serviço'
        context['ambiente'] = item.ambiente
        return context

    def form_valid(self, form):
        """
            Método que é executado ao submeter as informções para atualização.
            Pode ser utilizado para verificar as informções e fazer alterações antes da inserção no banco.
        """
        form.instance.casa = str(self.request.POST['casa']).upper()
        form.instance.ambiente = self.request.POST['ambiente']
        if(form.instance.quantidade == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.volume
        if(form.instance.volume == 0):
            form.instance.valor = form.instance.valorUnitario * form.instance.quantidade
        return super(Backup_dadosUpdate, self).form_valid(form)

class Backup_dadosDelete(DeleteView):
    """
        Classe que herda de DeleteView para implementar seus métodos no genrenciamento da página de exclusão de backups.
        Utilizado para dizer o model (atributos  que serão inseridos no banco) que será utilizado, página que deve ser direcionada após a inserção bem sucedida e outros campos.
    """
    model = Backup_dados
    success_url = reverse_lazy('servicos')

class Unidade:
    """
        Classe que possui os atributos de cada unidade.
        Se refere a tabela de Unidades do financeiro.
    """
    def __init__(self, unidade, qtd, porcentagem, valor):
        self.unidade = unidade
        self.qtd = qtd
        self.porcentagem = round(porcentagem, 2)
        self.valor = round(valor,2)