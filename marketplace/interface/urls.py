from django.urls import path
from .views import (
    UsuarioView, 
    UnidadResidencialView, 
    CategoriaView, 
    PublicarProductoView
)

urlpatterns = [
    path('usuarios/', UsuarioView.as_view(), name='usuarios-list-create'),
    path('unidades/', UnidadResidencialView.as_view(), name='unidades-list-create'),
    path('categorias/', CategoriaView.as_view(), name='categorias-list-create'),
    path('publicar-producto/', PublicarProductoView.as_view(), name='publicar-producto'),
]
