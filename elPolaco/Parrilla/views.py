from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Producto, Pedido, Mesa
from .forms import PedidoForm


def ver_menu(request):
    categoria = request.GET.get('categoria')  # Obtener la categoría seleccionada desde la URL
    if categoria:
        productos = Producto.objects.filter(categoria=categoria)  # Filtrar por categoría seleccionada
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no se selecciona categoría

    # Obtener todas las categorías para el select
    categorias = Producto._meta.get_field('categoria').choices

    return render(request, 'Parrilla/menu.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria  # Para que el select recuerde la categoría seleccionada
    })

# Vista para crear un nuevo pedido
class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Parrilla/crear_pedido.html'
    
    def form_valid(self, form):
        # Aquí podemos agregar lógica adicional si es necesario
        return super().form_valid(form)

# Vista para editar un pedido
class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Parrilla/editar_pedido.html'
    
    def form_valid(self, form):
        # Aquí podemos agregar lógica adicional si es necesario
        return super().form_valid(form)

# Vista para eliminar un pedido
class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'eliminar_pedido.html'
    success_url = reverse_lazy('listar_pedidos')

def vista_mesas(request):
    # Obtener todas las mesas
    mesas = Mesa.objects.all()
    return render(request, 'Parrilla/mesas.html', {'mesas': mesas})
    
def detalle_pedido(request, pedido_id):
    # Obtener el pedido por su ID
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'Parrilla/detalle_pedido.html', {'pedido': pedido})