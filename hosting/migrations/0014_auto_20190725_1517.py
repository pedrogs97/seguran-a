# Generated by Django 2.2.3 on 2019-07-25 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0013_auto_20190725_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='hosting',
            name='hosting_fieb',
            field=models.BooleanField(blank=True, default=False, verbose_name='Hosting SENAI'),
        ),
        migrations.AddField(
            model_name='hosting',
            name='hosting_senai',
            field=models.BooleanField(blank=True, default=False, verbose_name='Hosting SENAI'),
        ),
        migrations.AlterField(
            model_name='backup_dados',
            name='descricao',
            field=models.CharField(max_length=50, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='backup_dados',
            name='valorUnitario',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor Unitário'),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='descricao',
            field=models.CharField(blank=True, max_length=150, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='memoria',
            field=models.IntegerField(default=0, verbose_name='Memória'),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='tipo_maq',
            field=models.CharField(blank=True, max_length=20, verbose_name='Tipo de Máquina'),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='descricao',
            field=models.CharField(max_length=50, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='duracao',
            field=models.CharField(blank=True, default='-', max_length=150, verbose_name='Duração'),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='observacao',
            field=models.CharField(blank=True, default='-', max_length=150, verbose_name='Observação'),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='responsavel',
            field=models.CharField(blank=True, default='-', max_length=150, verbose_name='Responsável'),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='ticket',
            field=models.CharField(blank=True, default='-', max_length=150),
        ),
        migrations.AlterField(
            model_name='servicos_adicionais',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
