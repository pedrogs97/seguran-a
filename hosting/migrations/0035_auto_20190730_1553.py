# Generated by Django 2.2.3 on 2019-07-30 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0034_delete_financeiro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosting',
            name='mes',
            field=models.CharField(blank=True, default='July', max_length=12),
        ),
    ]
