from django.contrib import admin
from .models import Item, Pedido

class ItemInline(admin.TabularInline):
    model = Pedido.itens.through
    extra = 1 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    fields = ('user',)  

admin.site.register(Item)
