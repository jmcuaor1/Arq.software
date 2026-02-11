from marketplace.domain.usuario import Usuario
from marketplace.domain.categoria import Categoria
from marketplace.application.services import PublicacionService, PublicarProductoCommand
from marketplace.infrastructure.repositories import InMemoryProductoRepository

def main():
    repo = InMemoryProductoRepository()
    service = PublicacionService(repo)

    vendedor = Usuario("u-1", "María García", "maria@email.com", "0101", "+573001112233")
    categoria = Categoria("cat-1", "Hogar", "Artículos para el hogar")

    cmd = PublicarProductoCommand(
        vendedor=vendedor,
        vendedor_status="APPROVED",
        nombre="Silla de oficina",
        descripcion="Silla cómoda para escritorio, en buen estado, poco uso.",
        precio=120000,
        categoria=categoria,
        imagenes=[
            "https://img.fake/silla1.jpg",
            "https://img.fake/silla2.jpg",
        ],
    )

    producto = service.publicar_producto(cmd)

    print("[OK] Producto publicado vía Service Layer:", producto.id)
    print("[OK] Productos guardados:", [p.nombre for p in repo.list_all()])

if __name__ == "__main__":
    main()
