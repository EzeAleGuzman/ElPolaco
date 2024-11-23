from django.contrib import admin
from .models import Producto, Pedido, Mesa, DetallePedido


admin.site.register(Producto)
admin.site.register(Mesa)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
