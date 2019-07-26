from django.db import models

# Create your models here.
class Hosting(models.Model):
    empresa = models.CharField(max_length=50)
    server = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150, blank=True, verbose_name="Descrição")
    cpu = models.IntegerField(default=0)
    memoria = models.IntegerField(default=0, verbose_name="Memória")
    disco = models.IntegerField(default=0)
    tipo_maq = models.CharField(max_length=20, blank=True, verbose_name="Tipo de Máquina")
    tipo = models.IntegerField(blank=True)
    perfil = models.CharField(max_length=20)
    recurso = models.CharField(max_length=20, blank=True)
    valor_tabela = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    proc_adicional = models.IntegerField(blank=True, default=0)
    valor_proc_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    memoria_adicional = models.IntegerField(blank=True, default=0)
    valor_memoria_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    disco_adicional = models.IntegerField(blank=True, default=0)
    valor_disco_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    valor_total = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    hosting_senai = models.BooleanField(verbose_name="Hosting SENAI", blank=True, default=False)
    hosting_fieb = models.BooleanField(verbose_name="Hosting FIEB", blank=True, default=False)

class Servicos_adicionais(models.Model):
    casa = models.CharField(max_length=50, blank=True)
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    ticket = models.CharField(max_length=150, blank=True, default='-')
    duracao = models.CharField(max_length=150, blank=True, default='-', verbose_name="Duração")
    observacao = models.CharField(max_length=150, blank=True, default='-', verbose_name="Observação")
    responsavel = models.CharField(max_length=150, blank=True, default='-', verbose_name="Responsável")
    valor = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0.00)

class Backup_dados(models.Model):
    casa = models.CharField(max_length=50, blank=True)
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    valorUnitario = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0.00, verbose_name="Valor Unitário")
    volume = models.DecimalField(max_digits=12,decimal_places=2, blank=True, default=0.00)
    quantidade = models.IntegerField(blank=True, default=0)
    valor = models.DecimalField(max_digits=10,decimal_places=2, blank=True)

# class Precos(models.Model):
