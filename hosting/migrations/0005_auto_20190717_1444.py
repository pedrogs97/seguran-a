# Generated by Django 2.2.3 on 2019-07-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0004_auto_20190717_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosting',
            name='disco_adicional',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='memoria_adicional',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='proc_adicional',
            field=models.IntegerField(blank=True),
        ),
    ]
