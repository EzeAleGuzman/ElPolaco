from django.urls import path
from . import views


urlpatterns = [
    path('', views.ver_menu, name='ver_menu'),
]