# Generated by Django 2.2.3 on 2019-07-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0006_servicos_adicionais'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicos_adicionais',
            name='casa',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]