# Generated by Django 2.2.3 on 2019-08-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0045_auto_20190815_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='hosting',
            name='linux',
            field=models.BooleanField(blank=True, default=False, verbose_name='Servidor Linux'),
        ),
    ]
