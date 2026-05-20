from django.urls import path
from .views import (
    UsuarioView,
    UnidadResidencialView,
    CategoriaView,
    ProductoListView,
    ServicioView,
    ConsultaView,
    GenerarDescripcionView,
    CatalogoPublicoView,
    DatosAliadoView,
    ResponderConsultaView,
)

urlpatterns = [
    # Core marketplace
    path('usuarios/', UsuarioView.as_view(), name='usuarios-list-create'),
    path('unidades/', UnidadResidencialView.as_view(), name='unidades-list-create'),
    path('categorias/', CategoriaView.as_view(), name='categorias-list-create'),
    path('productos/', ProductoListView.as_view(), name='productos-list-create'),
    path('servicios/', ServicioView.as_view(), name='servicios-list-create'),
    path('consultas/', ConsultaView.as_view(), name='consultas-list-create'),
    path('consultas/<str:consulta_id>/responder/', ResponderConsultaView.as_view(), name='consultas-responder'),

    # Adapter Pattern — Google Gemini AI
    path('ai/generar-descripcion/', GenerarDescripcionView.as_view(), name='ai-generar-descripcion'),

    # Servicio aliado
    path('aliado/catalogo/', CatalogoPublicoView.as_view(), name='aliado-catalogo'),
    path('aliado/datos-externos/', DatosAliadoView.as_view(), name='aliado-datos-externos'),
]
