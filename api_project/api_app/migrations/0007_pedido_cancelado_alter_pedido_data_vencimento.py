# Generated by Django 4.2.5 on 2023-09-28 21:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0006_alter_pedido_data_vencimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cancelado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_vencimento',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 18, 41, 2, 914422)),
        ),
    ]