from django.db import models

# Create your models here.
class Hosting(models.Model):
    empresa = models.CharField(max_length=50)
    server = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150, blank=True)
    cpu_mf = models.IntegerField()
    memoria_mf = models.IntegerField()
    disco = models.IntegerField()
    tipo_maq = models.CharField(max_length=20)
    cpu_mv = models.IntegerField()
    memoria_mv = models.IntegerField()
    tipo = models.IntegerField()
    perfil = models.CharField(max_length=20)
    recurso = models.CharField(max_length=20)
    valor_tabela = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    proc_adicional = models.IntegerField()
    valor_proc_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    memoria_adicional = models.IntegerField()
    valor_memoria_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    disco_adicional = models.IntegerField()
    valor_disco_adicional = models.DecimalField(max_digits=10,decimal_places=2, blank=True)
    valor_total = models.DecimalField(max_digits=10,decimal_places=2, blank=True)

        
        