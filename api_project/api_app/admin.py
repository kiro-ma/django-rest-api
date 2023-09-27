from django.contrib import admin
from .models import Item, Pedido, PedidoItem
from django.db.models import Sum, F, DecimalField

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline]
    fields = ('user', 'quantidade_de_itens_em_pedidos', 'preco_total', 'data_criacao', 'data_vencimento', 'status_pagamento')
    readonly_fields = ('quantidade_de_itens_em_pedidos', 'preco_total',)
    list_display = ('user', 'quantidade_de_itens_em_pedidos', 'preco_total',)

    def quantidade_de_itens_em_pedidos(self, obj):
        # Calcula a quantidade total de itens em pedidos para este pedido
        total_quantidade = PedidoItem.objects.filter(pedido=obj).aggregate(Sum('quantidade'))['quantidade__sum']
        return total_quantidade if total_quantidade is not None else 0

    def preco_total(self, obj):
        # Calcula o preço total do pedido
        total_preco = PedidoItem.objects.filter(pedido=obj).aggregate(
            total=Sum(F('quantidade') * F('item__preco'), output_field=DecimalField())
        )['total']
        
        return 'R$ ' + str(total_preco) if total_preco is not None else 'R$ 0.00'

    preco_total.short_description = 'Preço Total do Pedido'

    quantidade_de_itens_em_pedidos.short_description = 'Quantidade de Itens em Pedidos'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')

# admin.site.unregister(Pedido.itens.through)  # Desregistra a tabela intermediária para evitar duplicatas no admin
