from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Producto, Pedido, Mesa, DetallePedido
from .forms import DetallePedidoForm
from django.db.models import Sum


def ver_menu(request):
    categoria = request.GET.get("categoria")
    if categoria:
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.all()
    categorias = Producto._meta.get_field("categoria").choices

    return render(
        request,
        "Parrilla/menu.html",
        {
            "productos": productos,
            "categorias": categorias,
            "categoria_seleccionada": categoria,
        },
    )


def crear_pedido(request):
    if request.method == "POST":
        mesa_id = request.POST.get("mesa_id")
        nombre = request.POST.get("nombre")
        mesa = get_object_or_404(Mesa, id=mesa_id)

        pedido = Pedido.objects.create(
            mesa=mesa,
            nombre=nombre,
            total=0,
            pagado=False,
            para_llevar=False,
        )
        mesa.estado = "ocupada"
        mesa.save()

        return redirect("vista_mesas")

    return render(request, "error.html")


def pagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        pedido.pagado = True
        pedido.save()

        mesa = pedido.mesa
        mesa.estado = "libre"
        mesa.save()

        return redirect("vista_mesas")

    return redirect("vista_mesas")


def cobrar_pedido(request, pk):
    # Obtener el pedido por su ID
    pedido = get_object_or_404(Pedido, pk=pk)

    # Marcar el pedido como pagado
    pedido.pagado = True
    pedido.save()

    # Redirigir al listado de pedidos para llevar
    return redirect("pedidos_para_llevar")


def pedidos_para_llevar(request):
    # Obtener todos los pedidos marcados como para llevar
    pedidos_para_llevar = Pedido.objects.filter(para_llevar=True, pagado=False)

    if request.method == "POST":
        # Crear un nuevo pedido para llevar
        nombre_cliente = request.POST.get("nombre_cliente", "")
        pedido = Pedido.objects.create(nombre=nombre_cliente, para_llevar=True)
        return redirect("pedidos_para_llevar")  # Redirigir a la misma página

    return render(
        request,
        "Parrilla/pedidos_para_llevar.html",
        {"pedidos_para_llevar": pedidos_para_llevar},
    )


def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)  # Usar pk directamente
    detalles_pedido = (
        pedido.detallepedido_set.all()
    )  # Obtener todos los detalles del pedido
    detalle_form = DetallePedidoForm()

    if request.method == "POST":
        detalle_form = DetallePedidoForm(request.POST)
        if detalle_form.is_valid():
            # Obtener el producto y la cantidad del formulario
            producto = detalle_form.cleaned_data["producto"]
            cantidad = detalle_form.cleaned_data["cantidad"]

            # Verificar si ya existe un detalle con el mismo producto en el pedido
            detalle_existente = pedido.detallepedido_set.filter(
                producto=producto
            ).first()

            if detalle_existente:
                # Si existe, actualiza la cantidad y el subtotal
                detalle_existente.cantidad += cantidad
                detalle_existente.subtotal = (
                    detalle_existente.producto.precio * detalle_existente.cantidad
                )
                detalle_existente.save()

                # Actualiza el total del pedido
                pedido.total += producto.precio * cantidad
                pedido.save()

            else:
                # Si no existe, crear un nuevo detalle
                detalle_pedido = detalle_form.save(commit=False)
                detalle_pedido.pedido = pedido
                detalle_pedido.save()

                # Actualiza el total del pedido
                pedido.total += detalle_pedido.producto.precio * detalle_pedido.cantidad
                pedido.save()

            # Redirigir a la misma vista con el pedido actualizado
            return redirect("editar_pedido", pk=pedido.pk)

    return render(
        request,
        "Parrilla/editar_pedido.html",
        {
            "pedido": pedido,
            "detalles_pedido": detalles_pedido,
            "detalle_form": detalle_form,
        },
    )


# Vista para eliminar un pedido
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()  # Elimina el pedido de la base de datos
    return redirect(
        "lista_pedidos"
    )  # Redirige a la vista de lista de pedidos o la que desees


def vista_mesas(request):
    # Obtener todas las mesas
    mesas = Mesa.objects.all()
    return render(request, "Parrilla/mesas.html", {"mesas": mesas})


def detalle_pedido(request, pedido_id):
    # Obtener el pedido por su ID
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "Parrilla/detalle_pedido.html", {"pedido": pedido})


def eliminar_detalle(request, detalle_id, pedido_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Actualiza el total del pedido al eliminar el detalle
    pedido.total -= detalle.producto.precio * detalle.cantidad
    pedido.save()

    # Elimina el detalle del pedido
    detalle.delete()

    # Redirige de vuelta a la página de edición del pedido
    return redirect("editar_pedido", pk=pedido.id)


def pedidos_administrador(request):
    # Filtrar los pedidos por la fecha actual (si no se pasa un día específico)
    fecha = request.GET.get(
        "fecha", timezone.now().date()
    )  # Obtener la fecha de la query parameter (default: hoy)

    # Filtrar los pedidos por la fecha seleccionada
    pedidos = Pedido.objects.filter(fecha__date=fecha)

    # Paginación: 20 pedidos por página
    paginator = Paginator(pedidos, 20)  # 20 pedidos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Calcular el total de facturación diaria
    total_facturacion = (
        pedidos.aggregate(total_facturacion=Sum("total"))["total_facturacion"] or 0
    )

    return render(
        request,
        "Parrilla/administracion.html",
        {
            "page_obj": page_obj,
            "fecha": fecha,
            "total_facturacion": total_facturacion,
        },
    )
