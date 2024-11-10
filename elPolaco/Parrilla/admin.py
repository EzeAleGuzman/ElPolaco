from django.contrib import admin
from .models import Producto, Mesa, Pedido

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria')  # Campos que se mostrarán en la lista de productos
    search_fields = ('nombre',)  # Permitir la búsqueda por nombre

class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado')

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('mesa', 'fecha_pedido', 'total', 'pagado')
    list_filter = ('pagado',)  # Filtro por estado de pago

# Registra los modelos para que aparezcan en el admin
admin.site.register(Producto)
admin.site.register(Mesa)
admin.site.register(Pedido)