# Generated by Django 2.2.3 on 2019-07-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0031_remove_hosting_teste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosting',
            name='mes',
            field=models.CharField(max_length=12,default='July'),
        ),
    ]