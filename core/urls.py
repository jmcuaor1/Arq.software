from django.urls import path
from marketplace.interface.views import (
    UsuarioView,
    CategoriaView,
    ProductoListView,
    ServicioView,
    ConsultaView
)
from django.views.generic import TemplateView

urlpatterns = [
    # Frontend Page
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # API Endpoints
    path('api/usuarios/', UsuarioView.as_view(), name='api_usuarios'),
    path('api/categorias/', CategoriaView.as_view(), name='api_categorias'),
    path('api/productos/', ProductoListView.as_view(), name='api_productos'),
    path('api/servicios/', ServicioView.as_view(), name='api_servicios'),
    path('api/consultas/', ConsultaView.as_view(), name='api_consultas'),
]
