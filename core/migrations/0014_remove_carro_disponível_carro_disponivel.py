# Generated by Django 4.2.1 on 2023-06-10 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_carro_disponível'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carro',
            name='disponível',
        ),
        migrations.AddField(
            model_name='carro',
            name='disponivel',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Disponível?'),
        ),
    ]
