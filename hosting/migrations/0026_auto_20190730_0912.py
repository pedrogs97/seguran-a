# Generated by Django 2.2.3 on 2019-07-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0025_auto_20190730_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='json',
            name='json',
            field=models.TextField(max_length=200),
        ),
    ]