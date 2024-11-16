from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Producto, Pedido, Mesa
from .forms import PedidoForm, DetallePedidoForm


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
    
    def form_invalid(self, form):
        # Si el formulario es inválido, redirigimos a la vista de mesas (puedes ajustar la URL según sea necesario)
        return redirect('vista_mesas')  # Asumiendo que 'lista_mesas' es el nombre de la URL que muestra las mesas

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    # Formulario para editar el pedido
    if request.method == 'POST' and 'editar_pedido' in request.POST:
        pedido_form = PedidoForm(request.POST, instance=pedido)
        if pedido_form.is_valid():
            pedido_form.save()
            pedido.calcular_total()  # Calcular el total después de editar
            return redirect('vista_mesas')
    else:
        pedido_form = PedidoForm(instance=pedido)

    # Formulario para agregar detalles al pedido
    if request.method == 'POST' and 'agregar_detalle' in request.POST:
        detalle_form = DetallePedidoForm(request.POST)
        if detalle_form.is_valid():
            detalle = detalle_form.save(commit=False)
            detalle.pedido = pedido  # Asociar el detalle con el pedido
            detalle.calcular_subtotal()  # Calcular el subtotal del detalle
            detalle.save()
            pedido.calcular_total()  # Recalcular el total después de agregar el detalle
            return redirect('editar_pedido', pk=pedido.id)
    else:
        detalle_form = DetallePedidoForm()

    detalles_pedido = pedido.detallepedido_set.all()  # Obtener los detalles del pedido

    return render(request, 'Parrilla/editar_pedido.html', {
        'pedido_form': pedido_form,
        'detalle_form': detalle_form,
        'detalles_pedido': detalles_pedido,
        'pedido': pedido,
    })

# Vista para eliminar un pedido
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()  # Elimina el pedido de la base de datos
    return redirect('lista_pedidos')  # Redirige a la vista de lista de pedidos o la que desees

def vista_mesas(request):
    # Obtener todas las mesas
    mesas = Mesa.objects.all()
    return render(request, 'Parrilla/mesas.html', {'mesas': mesas})
    
def detalle_pedido(request, pedido_id):
    # Obtener el pedido por su ID
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'Parrilla/detalle_pedido.html', {'pedido': pedido})