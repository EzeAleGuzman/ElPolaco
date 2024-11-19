from django.urls import path
from . import views


urlpatterns = [
    path("", views.ver_menu, name="ver_menu"),
    path("mesas/", views.vista_mesas, name="vista_mesas"),
    path("pedido/<int:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
    path("crear/", views.crear_pedido, name="crear_pedido"),
    path("pagar-pedido/<int:pedido_id>/", views.pagar_pedido, name="pagar_pedido"),
    path("editar/<int:pk>/", views.editar_pedido, name="editar_pedido"),
    path("eliminar/<int:pedido_id>/", views.eliminar_pedido, name="eliminar_pedido"),
    path(
        "eliminar-detalle/<int:detalle_id>/<int:pedido_id>/",
        views.eliminar_detalle,
        name="eliminar_detalle",
    ),
    path("pedidos-para-llevar/", views.pedidos_para_llevar, name="pedidos_para_llevar"),
    path("cobrar/<int:pk>/", views.cobrar_pedido, name="cobrar_pedido"),
    path(
        "pedidos-administrador/",
        views.pedidos_administrador,
        name="pedidos_administrador",
    ),
]
