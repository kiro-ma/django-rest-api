from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Item(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.FloatField(default=0)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

# Esse Model serve para saber as quantidades de cada item do Pedido
class PedidoItem(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='itens_pedido', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pedido.id} - {self.item.nome} x{self.quantidade}'

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_vencimento = models.DateTimeField(default=timezone.now)
    status_pagamento = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

