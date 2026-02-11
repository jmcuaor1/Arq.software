import json
from django.http import JsonResponse
from django.views import View
from ..application.services import PublicacionService, PublicarProductoCommand
from ..domain.usuario import Usuario
from ..domain.categoria import Categoria
from ..infrastructure.repositories import InMemoryProductoRepository

_repo = InMemoryProductoRepository()
_service = PublicacionService(_repo)

class PublicarProductoView(View):
    def post(self, request):
        data = json.loads(request.body)

        vendedor = Usuario(**data["vendedor"])
        categoria = Categoria(**data["categoria"])

        cmd = PublicarProductoCommand(
            vendedor=vendedor,
            vendedor_status=data["vendedor_status"],
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            precio=data["precio"],
            categoria=categoria,
            imagenes=data["imagenes"]
        )

        producto = _service.publicar_producto(cmd)

        return JsonResponse({"ok": True, "producto_id": producto.id})
