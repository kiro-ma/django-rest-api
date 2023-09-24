from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.FloatField(default=0)

    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    itens = models.ManyToManyField(Item)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

