# Generated by Django 2.2.3 on 2019-07-29 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0018_financeiro'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeiro',
            name='tabela',
            field=models.CharField(default='', max_length=50),
        ),
    ]