# Generated by Django 4.2.5 on 2023-09-27 21:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0004_remove_pedido_itens'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pedido',
            name='data_vencimento',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pedido',
            name='status_pagamento',
            field=models.BooleanField(default=False),
        ),
    ]
