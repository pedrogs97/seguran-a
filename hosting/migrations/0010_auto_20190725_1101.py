# Generated by Django 2.2.3 on 2019-07-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0009_auto_20190725_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup_dados',
            name='quantidade',
            field=models.IntegerField(blank=True),
        ),
    ]