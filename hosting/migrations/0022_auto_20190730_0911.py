# Generated by Django 2.2.3 on 2019-07-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0021_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='json',
            name='json',
            field=models.CharField(max_length=200),
        ),
    ]
