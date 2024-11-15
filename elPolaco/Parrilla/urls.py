from django.urls import path
from . import views


urlpatterns = [
    path('', views.ver_menu, name='ver_menu'),
    path('mesas/', views.vista_mesas, name='vista_mesas'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('crear/', views.PedidoCreateView.as_view(), name='crear_pedido'),
    path('editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),
    path('eliminar/<int:pk>/', views.PedidoDeleteView.as_view(), name='eliminar_pedido'),
]