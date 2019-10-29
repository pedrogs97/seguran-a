from .models import Hosting
import datetime

class Auxiliares:
    """
        Classe que auxilia nas informações que serão exibidas pela view.
    """
    @staticmethod
    def disc_adicional(disco, is_linux, tipo):
        """
            Retorna a diferença entre a quantidade de disco que possui na vm e quanto é o plano disponibiliza.
        """
        if is_linux :
            if tipo == 3 :
                return disco - 250
            elif tipo == 2 :
                return disco - 100
            else :
                return disco - 50
        else:
            return disco - 80
    @staticmethod
    def mem_adicional(tipo, mem, is_linux):
        """
            Retorna a diferença entre a quantidade de memoria que possui na vm e quanto é o plano disponibiliza.
        """
        if is_linux :
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
    @staticmethod
    def cpu_adicional(tipo, cpu, is_linux):
        """
            Retorna a diferença entre a quantidade de cpu que possui na vm e quanto é o plano disponibiliza.
        """
        if is_linux :
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
    @staticmethod
    def recurso(tipo):
        """
            Retorna o recurso de máquina que será cobrado de acordo com o tipo de máquina selecionada.
        """
        if(tipo == 1):
            return 'BÁSICO'
        if(tipo == 2):
            return 'INTERMEDIÁRIO'
        else:
            return 'AVANÇADO'
    @staticmethod
    def valor_tabela(maq, perfil, recurso):
        """
            Retorna o valor tabelado de acordo com perfil e recurso da máquina específicada.
        """
        if(perfil == 'GOLD'):
            if(recurso == 'BÁSICO'):
                return 365.62
            if(recurso == 'INTERMEDIÁRIO'):
                return 581.08
            if(recurso == 'AVANÇADO'):
                if(maq == 'Fisico'):
                    return 2816.55
                else:
                    return 1022.02
        if(perfil == 'PLATINUM'):
            if(recurso == 'BÁSICO'):
                return 548.43
            if(recurso == 'INTERMEDIÁRIO'):
                return 871.62
            if(recurso == 'AVANÇADO'):
                return 1533.04
    @staticmethod
    def tipo(cpu, mem, is_linux):
        """
            Retorna o tipo de máquina de acordo com os tipos de cpu e memória.
            1- Básico
            2- Intermediário
            3- Avançado
        """
        tipo_cpu = 1
        tipo_mem = 1
        if is_linux :
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
    @staticmethod
    def get_years():
        """
            Retorna todos os anos que tiveram um server adicionado.
        """
        anos = []
        for item in Hosting.objects.all():
                if anos.__len__() == 0:
                    if(item.data_insert is None):
                        continue
                    anos.append(item.data_insert.year)
                if(anos.count(item.data_insert.year) == 0) :
                    anos.append(item.data_insert.year)
        
        return anos
    @staticmethod
    def valor_ordenar(hosting):
        """
            Retorna o valor que irá ordenar a lista de hosting.
        """
        return hosting.valor_total
    @staticmethod
    def empresas(hosting_list):
        """
            Retorna um dicionário de empresa e o valor de todos os servidores.
        """
        list_emp = []
        list_dic_emp = []
        for item in hosting_list:
            if(list_emp is None):
                list_emp.append(item.empresa)
            if(list_emp.count(item.empresa) == 0 ):
                list_emp.append(item.empresa)

        for empresa in list_emp :
            dic = {}
            dic['empresa'] = empresa
            total_empresa = 0
            for item in hosting_list :
                if(empresa == item.empresa) :
                    total_empresa = item.valor_total + total_empresa
            dic['valor'] = total_empresa
            list_dic_emp.append(dic)

        return list_dic_emp
    @staticmethod
    def valor_disco_adicional(qtd_disc, perfil):
        """
            Método que retorna o valor de disco adicional.
        """
        if perfil == 'PLATINUM' :
            return round(qtd_disc * 1.056, 2)
        else:
            return round(qtd_disc * 0.704, 2)
    @staticmethod
    def valor_mem_adicional(qtd_mem):
        """
            Método que retorna o valor de memória adicional.
        """
        return round(qtd_mem * 54.904, 2)
    @staticmethod
    def valor_proc_adicional(qtd_proc, perfil):
        """
            Método que retorna o valor de CPU adicional.
        """
        if perfil == 'PLATINUM' :
            return round(qtd_proc * 80.2675, 2)
        else:
            return round(qtd_proc * 53.512, 2)
    @staticmethod
    def somar_servicos(list_serv, list_backup, **kwargs):
        """
            Método que retorna um dicionário com o valores totais de cada casa (fieb, iel, senai, sesi) e geral.
            Recebe as listas com cada item - backup e serviço e kwargs, se o tipo for 'mes' é obrigatório os campos: inicial, final e ano.
        """
        date = datetime.date(year = 2000, month= 1, day = 1)
        total_servico = 0
        total_backup = 0
        total_casa_senai = 0
        total_casa_fieb = 0
        total_casa_sesi = 0
        total_casa_iel = 0
        
        if kwargs :
            if kwargs['tipo'] == 'mes':
                return Auxiliares.valor_mes_serv(list_serv, list_backup)
            else:
                return Auxiliares.valor_mes_serv(list_serv, list_backup, tipo=kwargs['tipo'], inicial=int(kwargs['inicial']), final=int(kwargs['final']), ano=int(kwargs['ano']))
        else:
            for item in list_backup :
                if item.casa == 'SENAI' and item.data_delete == date :
                    total_casa_senai += item.valor
                if item.casa == 'FIEB' and item.data_delete == date :
                    total_casa_fieb += item.valor
                if item.casa == 'SESI' and item.data_delete == date :
                    total_casa_sesi += item.valor
                if item.casa == 'IEL' and item.data_delete == date :
                    total_casa_iel += item.valor
                total_backup += item.valor

            for item in list_serv :
                if item.casa == 'SENAI' and item.data_delete == date :
                    total_casa_senai += item.valor
                if item.casa == 'FIEB' and item.data_delete == date :
                    total_casa_fieb += item.valor
                if item.casa == 'SESI' and item.data_delete == date :
                    total_casa_sesi += item.valor
                if item.casa == 'IEL' and item.data_delete == date :
                    total_casa_iel += item.valor
                total_servico += item.valor

            return {'fieb': total_casa_fieb, 'iel': total_casa_iel, 'senai': total_casa_senai, 'sesi': total_casa_sesi, 'servico': total_servico, 'backup': total_backup, 'total': total_servico + total_backup}
    @staticmethod
    def dic_meses():
        """
            Método que retorna um dicionário com mes(key) e valor(value).
        """
        dic = {'jan': 0,'fev': 0,'mar': 0,'abr': 0,'maio': 0,'jun': 0,'jul': 0,'ago': 0,'set': 0,'out': 0,'nov': 0,'dez': 0}
        return dic
    @staticmethod
    def valor_mes_serv(list_serv, list_backup, **kwargs):
        """
            Método que calcula o valor total de todos os serviços, adicionais e backup.
            Recebe as listas de serviços adicionais e kwargs, se o tipo for 'pesquisa' é obrigatório os campos: inicial, final e ano.
            Retorna um dicionário com mes(key) e o valor total do mes em serviços(value).
        """
        valor_mes_servicosFSI = Auxiliares.dic_meses()
        valor_mes_servicos = Auxiliares.dic_meses()
        ano = datetime.date.today().year
            
        if not kwargs:
            for item in list_serv:
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year :
                    if (((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jan'] += item.valor
                    if (((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['fev'] += item.valor
                    if (((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['mar'] += item.valor
                    if (((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['abr'] += item.valor
                    if (((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            print('servico - ', item.valor)
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SESI':
                            print('servico - ', item.valor)
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'IEL':
                            print('servico - ', item.valor)
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['maio'] += item.valor
                    if (((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jun'] += item.valor
                    if (((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jul'] += item.valor
                    if (((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['ago'] += item.valor
                    if (((item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['set'] += item.valor
                    if (((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['out'] += item.valor
                    if (((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['nov'] += item.valor
                    if (((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['dez'] += item.valor

            for item in list_backup:
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year :
                    if (((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jan'] += item.valor
                    if (((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['fev'] += item.valor
                    if (((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['mar'] += item.valor
                    if (((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['abr'] += item.valor
                    if (((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['maio'] += item.valor
                    if (((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jun'] += item.valor
                    if (((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jul'] += item.valor
                    if (((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['ago'] += item.valor
                    if (((item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['set'] += item.valor
                    if (((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['out'] += item.valor
                    if (((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['nov'] += item.valor
                    if (((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['dez'] += item.valor

        elif kwargs['tipo'] == 'pesquisa' :
            mes_inicial = kwargs['inicial']
            mes_final = kwargs['final']
            ano = kwargs['ano']
            
            for item in list_serv:
                if(item.data_insert is None):
                    continue
                if ano == item.data_insert.year :
                    if ((((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10))) and (1 >=  mes_inicial and 1 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jan'] += item.valor
                    if ((((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10))) and (2 >=  mes_inicial and 2 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['fev'] += item.valor
                    if ((((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10))) and (3 >=  mes_inicial and 3 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['mar'] += item.valor
                    if ((((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10))) and (4 >=  mes_inicial and 4 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['abr'] += item.valor
                    if ((((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10))) and (5 >=  mes_inicial and 5 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['maio'] += item.valor
                    if ((((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10))) and (6 >=  mes_inicial and 6 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jun'] += item.valor
                    if ((((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10))) and (7 >=  mes_inicial and 7 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jul'] += item.valor
                    if ((((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10))) and (8 >=  mes_inicial and 8 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['ago'] += item.valor
                    if ((((item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10))) and (9 >=  mes_inicial and 9 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['set'] += item.valor
                    if ((((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10))) and (10 >= mes_inicial and 10 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['out'] += item.valor
                    if ((((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10))) and (11 >=  mes_inicial and 11 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['nov'] += item.valor
                    if ((((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1))) and (12 >=  mes_inicial and 12 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['dez'] += item.valor
            
            for item in list_backup:
                
                if(item.data_insert is None):
                    continue
                if ano == item.data_insert.year :
                    if ((((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10))) and (1 >=  mes_inicial and 1 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jan'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jan'] += item.valor
                    if ((((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10))) and (2 >=  mes_inicial and 2 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['fev'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['fev'] += item.valor
                    if ((((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10))) and (3 >=  mes_inicial and 3 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['mar'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['mar'] += item.valor
                    if ((((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10))) and (4 >=  mes_inicial and 4 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['abr'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['abr'] += item.valor
                    if ((((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10))) and (5 >=  mes_inicial and 5 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['maio'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['maio'] += item.valor
                    if ((((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10))) and (6 >=  mes_inicial and 6 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jun'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jun'] += item.valor
                    if ((((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10))) and (7 >=  mes_inicial and 7 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['jul'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['jul'] += item.valor
                    if ((((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10))) and (8 >=  mes_inicial and 8 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['ago'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['ago'] += item.valor
                    if ((((item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10))) and (9 >=  mes_inicial and 9 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['set'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['set'] += item.valor
                    if ((((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10))) and (10 >= mes_inicial and 10 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['out'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['out'] += item.valor
                    if ((((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10))) and (11 >=  mes_inicial and 11 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['nov'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['nov'] += item.valor
                    if ((((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1))) and (12 >=  mes_inicial and 12 <= mes_final ):
                        if item.casa == 'FIEB':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SESI':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'IEL':
                            valor_mes_servicosFSI['dez'] += item.valor
                        if item.casa == 'SENAI':
                            valor_mes_servicos['dez'] += item.valor
        return valor_mes_servicos, valor_mes_servicosFSI
    @staticmethod
    def valor_mes_nead_senai(list_hosting, **kwargs):
        """
            Método retorna 2 dicionáriosm ou 5, de mês/valor de hostings do senai, ou fieb.
            Recebe a lista de hosting e kwargs, se o tipo for 'pesquisa' é obrigatório os campos: inicial, final e ano, ambiente indica qual ambiente está, fieb ou senai.
        """
        valor_mes = Auxiliares.dic_meses()
        valor_mes_nead = Auxiliares.dic_meses()
        ano = datetime.date.today().year
        if kwargs:
            if 'tipo' in kwargs:
                mes_inicial = int(kwargs['inicial'])
                mes_final = int(kwargs['final'])
                ano = int(kwargs['ano'])
                if kwargs['tipo'] == 'pesquisa':
                    if 'ambiente' in kwargs:
                        valor_mes_fieb = Auxiliares.dic_meses()
                        valor_mes_sesi = Auxiliares.dic_meses()
                        valor_mes_iel = Auxiliares.dic_meses()
                        valor_mes_gti = Auxiliares.dic_meses()
                        if kwargs['ambiente'] == 'fieb':
                            for item in list_hosting:
                                if(item.data_insert is None):
                                    continue
                                if ano == item.data_insert.year :
                                    if ((((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10))) and (1 >=  mes_inicial and 1 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['jan'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['jan'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['jan'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['jan'] += item.valor_total
                                        valor_mes['jan'] += item.valor_total
                                    if ((((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10))) and (2 >=  mes_inicial and 2 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['fev'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['fev'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['fev'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['fev'] += item.valor_total
                                        valor_mes['fev'] += item.valor_total
                                    if ((((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10))) and (3 >=  mes_inicial and 3 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['mar'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['mar'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['mar'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['mar'] += item.valor_total
                                        valor_mes['mar'] += item.valor_total
                                    if ((((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10))) and (4 >=  mes_inicial and 4 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['abr'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['abr'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['abr'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['abr'] += item.valor_total
                                        valor_mes['abr'] += item.valor_total
                                    if ((((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10))) and (5 >=  mes_inicial and 5 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['maio'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['maio'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['maio'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['maio'] += item.valor_total
                                        valor_mes['maio'] += item.valor_total
                                    if ((((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10))) and (6 >=  mes_inicial and 6 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['jun'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['jun'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['jun'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['jun'] += item.valor_total
                                        valor_mes['jun'] += item.valor_total
                                    if ((((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10))) and (7 >=  mes_inicial and 7 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['jul'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['jul'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['jul'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['jul'] += item.valor_total
                                        valor_mes['jul'] += item.valor_total
                                    if ((((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10))) and (8 >=  mes_inicial and 8 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['ago'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['ago'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['ago'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['ago'] += item.valor_total
                                        valor_mes['ago'] += item.valor_total
                                    if ((((item.data_insert.month <= 9 and 9<= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10))) and (9 >=  mes_inicial and 9 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['set'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['set'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['set'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['set'] += item.valor_total
                                        valor_mes['set'] += item.valor_total
                                    if ((((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10))) and (10 >=  mes_inicial and 10 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['out'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['out'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['out'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['out'] += item.valor_total
                                        valor_mes['out'] += item.valor_total
                                    if ((((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10))) and (11 >=  mes_inicial and 11 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['nov'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['nov'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['nov'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['nov'] += item.valor_total
                                        valor_mes['nov'] += item.valor_total
                                    if ((((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1))) and (12 >=  mes_inicial and 12 <= mes_final ):
                                        if item.empresa == 'SENAI_GTI':
                                            valor_mes_gti['dez'] += item.valor_total
                                        if item.empresa == 'FIEB':
                                            valor_mes_fieb['dez'] += item.valor_total
                                        if item.empresa == 'IEL':
                                            valor_mes_iel['dez'] += item.valor_total
                                        if item.empresa == 'SESI':
                                            valor_mes_sesi['dez'] += item.valor_total
                                        valor_mes['dez'] += item.valor_total

                            return valor_mes, valor_mes_fieb, valor_mes_gti, valor_mes_iel, valor_mes_sesi
                    else:
                        for item in list_hosting:
                                if(item.data_insert is None):
                                    continue
                                if ano == item.data_insert.year :
                                    if ((((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10))) and (1 >=  mes_inicial and 1 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['jan'] += item.valor_total
                                        else:
                                            valor_mes['jan'] += item.valor_total
                                    if ((((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10))) and (2 >=  mes_inicial and 2 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['fev'] += item.valor_total
                                        else:
                                            valor_mes['fev'] += item.valor_total
                                    if ((((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10))) and (3 >=  mes_inicial and 3 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['mar'] += item.valor_total
                                        else:
                                            valor_mes['mar'] += item.valor_total
                                    if ((((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10))) and (4 >=  mes_inicial and 4 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['abr'] += item.valor_total
                                        else:
                                            valor_mes['abr'] += item.valor_total
                                    if ((((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10))) and (5 >=  mes_inicial and 5 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['maio'] += item.valor_total
                                        else:
                                            valor_mes['maio'] += item.valor_total
                                    if ((((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10))) and (6 >=  mes_inicial and 6 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['jun'] += item.valor_total
                                        else:
                                            valor_mes['jun'] += item.valor_total
                                    if ((((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10))) and (7 >=  mes_inicial and 7 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['jul'] += item.valor_total
                                        else:
                                            valor_mes['jul'] += item.valor_total
                                    if ((((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10))) and (8 >=  mes_inicial and 8 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['ago'] += item.valor_total
                                        else:
                                            valor_mes['ago'] += item.valor_total
                                    if ((((item.data_insert.month <= 9 and 9<= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10))) and (9 >=  mes_inicial and 9 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['set'] += item.valor_total
                                        else:
                                            valor_mes['set'] += item.valor_total
                                    if ((((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10))) and (10 >=  mes_inicial and 10 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['out'] += item.valor_total
                                        else:
                                            valor_mes['out'] += item.valor_total
                                    if ((((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10))) and (11 >=  mes_inicial and 11 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['nov'] += item.valor_total
                                        else:
                                            valor_mes['nov'] += item.valor_total
                                    if ((((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1))) and (12 >=  mes_inicial and 12 <= mes_final ):
                                        if item.empresa == 'NEAD':
                                            valor_mes_nead['dez'] += item.valor_total
                                        else:
                                            valor_mes['dez'] += item.valor_total
        else:
            for item in list_hosting:
                if(item.data_insert is None):
                        continue
                if ano == item.data_insert.year :
                    if (((item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 1 and (item.data_insert.month == 1 and 1 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 2 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jan'] += item.valor_total
                        else:
                            valor_mes['jan'] += item.valor_total
                    if (((item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 2 and (item.data_insert.month <= 2 and 2 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 3 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['fev'] += item.valor_total
                        else:
                            valor_mes['fev'] += item.valor_total
                    if (((item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 3 and (item.data_insert.month <= 3 and 3 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 4 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['mar'] += item.valor_total
                        else:
                            valor_mes['mar'] += item.valor_total
                    if (((item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 4 and (item.data_insert.month <= 4 and 4 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 5 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['abr'] += item.valor_total
                        else:
                            valor_mes['abr'] += item.valor_total
                    if (((item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 5 and (item.data_insert.month <= 5 and 5 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 6 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['maio'] += item.valor_total
                        else:
                            valor_mes['maio'] += item.valor_total
                    if (((item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 6 and (item.data_insert.month <= 6 and 6 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 7 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jun'] += item.valor_total
                        else:
                            valor_mes['jun'] += item.valor_total
                    if (((item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 7 and (item.data_insert.month <= 7 and 7 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 8 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['jul'] += item.valor_total
                        else:
                            valor_mes['jul'] += item.valor_total
                    if (((item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 8 and (item.data_insert.month <= 8 and 8 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 9 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['ago'] += item.valor_total
                        else:
                            valor_mes['ago'] += item.valor_total
                    if (((item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 9 and (item.data_insert.month <= 9 and 9 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 10 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['set'] += item.valor_total
                        else:
                            valor_mes['set'] += item.valor_total
                    if (((item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 10 and (item.data_insert.month <= 10 and 10 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 11 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['out'] += item.valor_total
                        else:
                            valor_mes['out'] += item.valor_total
                    if (((item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)) and item.data_delete.year == 2000) or (item.data_delete.month > 11 and (item.data_insert.month <= 11 and 11 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 12 and item.data_insert.day <= 10)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['nov'] += item.valor_total
                        else:
                            valor_mes['nov'] += item.valor_total
                    if (((item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)) and item.data_delete.year == 2000) or (item.data_delete.month > 12 and (item.data_insert.month <= 12 and 12 <= datetime.date.today().month and item.data_insert.day >= 11) or (item.data_insert.month == 1 and item.data_insert.day <= 10 and item.data_insert.year + 1 == datetime.date.today().year + 1)):
                        if item.empresa == 'NEAD':
                            valor_mes_nead['dez'] += item.valor_total
                        else:
                            valor_mes['dez'] += item.valor_total
        
        return valor_mes, valor_mes_nead
    @staticmethod
    def valor_medio(dic):
        """
            Método que retorna o valor médio dos valores de um dicionário.
        """
        count = 0
        total_servico = 0
        for key in dic:
            if dic[key] :
                count += 1
                total_servico += dic[key]

        if count != 0 :      
            return total_servico/count
        else :
            return 0
    @staticmethod
    def somar_total(*args,**kwargs) :
        """
            Método que realiza a soma dos valores de um, ou mais, dicionário-retorna a soma- ou realiza a soma dos valores de uma chave de um, ou mais, dicionário-retorna um dicionário com as somas em cada chave.
            Parametro: soma='mes' indica que a soma será dos valores de uma chave.
        """
        if kwargs :
            if 'soma_dic' in kwargs:
                dic_soma = Auxiliares.dic_meses()
                if kwargs['soma_dic']:
                    for key in dic_soma :
                        for dic in args:
                            dic_soma[key] += dic[key]                 
                return dic_soma
        else:
            soma = 0
            for dic in args:
                for value in dic.values():
                    soma += value
            return soma
    @staticmethod
    def search(mes, ano, hosting_list):
        hosting_list_search = []
        intMes = Auxiliares.mes_inteiro(mes)
        intAno = int(ano)
        for item in hosting_list:
            if (item.data_delete.month > intMes and item.data_delete.year >= intAno) or item.data_delete.year == 2000:
                hosting_list_search.append(item)

        return hosting_list_search
    @staticmethod
    def ordenar(tipo, teste):
        '''
            Realiza a ordenação de acordo com o tipo, crescente ou decrescente.
        '''
        if tipo == 'crescente':
            teste.sort(key=Auxiliares.valor_ordenar)
        elif tipo == 'decrescente' :
            teste.sort(reverse=True, key=Auxiliares.valor_ordenar) 
        return teste
    @staticmethod
    def mes_inteiro(mesStr):
        if mesStr == 'January':
            return 1
        elif mesStr == 'February':
            return 2 
        elif mesStr == 'March':
            return 3
        elif mesStr == 'April':
            return 4
        elif mesStr == 'May':
            return 5
        elif mesStr == 'June':
            return 6
        elif mesStr == 'July':
            return 7
        elif mesStr == 'August':
            return 8
        elif mesStr == 'September':
            return 9
        elif mesStr == 'October':
            return 10
        elif mesStr == 'November':
            return 11
        elif mesStr == 'December':
            return 12
    @staticmethod
    def mes_atual(data):
        for i in range(1,13):
            if (data.month == i and data.day >= 11) or (data.month == i+1 and data.day <= 10):
                return datetime.date(year=data.year,month=i,day=data.day)
            elif data.month == 1 and data.day <= 10:
                return datetime.date(year=data.year - 1,month=12,day=data.day)

        
