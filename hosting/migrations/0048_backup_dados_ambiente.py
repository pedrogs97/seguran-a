# Generated by Django 2.2.3 on 2019-10-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0047_servicos_adicionais_ambiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup_dados',
            name='ambiente',
            field=models.CharField(blank=True, default='', max_length=5, verbose_name='Ambiente'),
        ),
    ]
