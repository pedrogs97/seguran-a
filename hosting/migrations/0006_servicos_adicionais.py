# Generated by Django 2.2.3 on 2019-07-24 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0005_auto_20190717_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicos_adicionais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('ticket', models.CharField(blank=True, max_length=150)),
                ('duracao', models.CharField(blank=True, max_length=150)),
                ('observacao', models.CharField(blank=True, max_length=150)),
                ('responsavel', models.CharField(blank=True, max_length=150)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
            ],
        ),
    ]
