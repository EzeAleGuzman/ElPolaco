# from django.contrib import admin
# from .models import Producto, Pedido, Mesa, PedidoProducto

# class PedidoProductoInline(admin.TabularInline):
#     model = PedidoProducto
#     extra = 1  # Puedes agregar más productos por defecto

# class PedidoAdmin(admin.ModelAdmin):
#     inlines = [PedidoProductoInline]
#     list_display = ('mesa', 'fecha', 'total', 'pagado')
#     list_filter = ('pagado',)

# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'precio', 'categoria')
#     search_fields = ('nombre',)

# admin.site.register(Producto, ProductoAdmin)
# admin.site.register(Mesa)
# admin.site.register(Pedido, PedidoAdmin)
# admin.site.register(PedidoProducto)
