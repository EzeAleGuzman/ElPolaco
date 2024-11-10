from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto


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
