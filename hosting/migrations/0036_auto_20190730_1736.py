# Generated by Django 2.2.3 on 2019-07-30 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0035_auto_20190730_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hosting',
            name='mes',
        ),
        migrations.AddField(
            model_name='hosting',
            name='data_delet',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='hosting',
            name='data_insert',
            field=models.DateField(blank=True, default=None),
        ),
    ]