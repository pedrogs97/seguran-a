# Generated by Django 2.2.3 on 2019-10-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0046_hosting_linux'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicos_adicionais',
            name='ambiente',
            field=models.CharField(blank=True, default='', max_length=5, verbose_name='Ambiente'),
        ),
    ]
