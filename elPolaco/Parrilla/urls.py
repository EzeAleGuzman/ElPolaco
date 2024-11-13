from django.urls import path
from . import views


urlpatterns = [
    path('', views.ver_menu, name='ver_menu'),
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesa/reservar/<int:mesa_id>/', views.marcar_como_reservada, name='marcar_como_reservada'),
    path('mesa/liberar/<int:mesa_id>/', views.liberar_mesa, name='liberar_mesa'),
    path('pedido/nuevo/<int:mesa_id>/', views.crear_pedido, name='crear_pedido'),
]