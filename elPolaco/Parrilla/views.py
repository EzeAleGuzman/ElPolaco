from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Producto, Pedido, Mesa


# def ver_menu(request):
#     productos = Producto.objects.all()
#     return render(request, 'Parrilla/menu.html', {'productos': productos})

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

def crear_pedido(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # Crear un nuevo pedido solo si no hay uno pendiente
    pedido, created = Pedido.objects.get_or_create(mesa=mesa, pagado=False, defaults={'fecha': timezone.now()})
    
    if not created:
        return redirect('detalle_pedido', pedido_id=pedido.id)
    
    return redirect('lista_productos', pedido_id=pedido.id)


def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas.html', {'mesas': mesas})

def marcar_como_reservada(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.estado = 'reservada'
    mesa.save()
    return redirect('lista_mesas')

def liberar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.estado = 'libre'
    mesa.save()
    return redirect('lista_mesas')