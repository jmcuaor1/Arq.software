"""Demo del Marketplace de Unidades Residenciales."""

from marketplace import (
    UnidadResidencial,
    Marketplace,
    Usuario,
    Producto,
    Servicio,
    Categoria,
    Carrito,
    Transaccion,
)
from marketplace.carrito import ItemCarrito
from marketplace.transaccion import ItemTransaccion


def main():
    # 1. Crear Unidad Residencial
    torre_verde = UnidadResidencial(
        id="ur-001",
        nombre="Torre Verde",
        direccion="Calle 123 #45-67",
    )
    print(f"[OK] {torre_verde}")

    # 2. Crear Marketplace asociado
    mp = torre_verde.crear_marketplace("Compras Torre Verde")
    print(f"[OK] {mp}")

    # 3. Crear categorías
    cat_electronica = Categoria("cat-1", "Electrónica", "Dispositivos y accesorios")
    cat_hogar = Categoria("cat-2", "Hogar", "Artículos para el hogar")
    cat_servicios = Categoria("cat-3", "Servicios", "Servicios entre vecinos")
    mp.registrar_categoria(cat_electronica)
    mp.registrar_categoria(cat_hogar)
    mp.registrar_categoria(cat_servicios)
    print("[OK] Categorías registradas:", [c.nombre for c in mp.categorias])

    # 4. Crear usuarios/residentes
    maria = Usuario("u-1", "María García", "maria@email.com", "101", "3001112233")
    carlos = Usuario("u-2", "Carlos López", "carlos@email.com", "205", "3002223344")
    ana = Usuario("u-3", "Ana Martínez", "ana@email.com", "302")
    torre_verde.registrar_residente(maria)
    torre_verde.registrar_residente(carlos)
    torre_verde.registrar_residente(ana)
    print("[OK] Residentes:", [str(u) for u in torre_verde.residentes])

    # 5. Publicar productos
    laptop = Producto(
        id="p-1",
        nombre="Laptop usada",
        precio=850000,
        vendedor=maria,
        descripcion="Laptop HP en buen estado",
        stock=1,
        categoria=cat_electronica,
    )
    silla = Producto(
        id="p-2",
        nombre="Silla de oficina",
        precio=120000,
        vendedor=carlos,
        stock=2,
        categoria=cat_hogar,
    )
    mp.publicar_producto(laptop)
    mp.publicar_producto(silla)
    print("[OK] Productos:", [str(p) for p in mp.productos])

    # 6. Publicar servicios
    reparacion = Servicio(
        id="s-1",
        nombre="Reparación de computadores",
        precio=50000,
        proveedor=carlos,
        descripcion="Diagnóstico y reparación básica",
        disponible=True,
        categoria=cat_servicios,
    )
    babysitter = Servicio(
        id="s-2",
        nombre="Cuidado de niños",
        precio=25000,
        proveedor=ana,
        disponible=True,
    )
    mp.publicar_servicio(reparacion)
    mp.publicar_servicio(babysitter)
    print("[OK] Servicios:", [str(s) for s in mp.servicios])

    # 7. Ana agrega items al carrito
    carrito_ana = mp.obtener_carrito(ana)
    carrito_ana.agregar(silla, 1)
    carrito_ana.agregar(reparacion, 1)
    print(f"[OK] {carrito_ana}")
    for item in carrito_ana.items:
        print(f"   - {item}")

    # 8. Crear transacción desde el carrito
    items_transaccion = [
        ItemTransaccion(item=ic.item, cantidad=ic.cantidad, precio_unitario=ic.item.precio)
        for ic in carrito_ana.items
    ]
    transaccion = Transaccion(
        id="t-001",
        comprador=ana,
        items=items_transaccion,
    )
    transaccion.confirmar()
    mp.registrar_transaccion(transaccion)
    carrito_ana.vaciar()
    print(f"[OK] {transaccion}")

    # 9. Búsquedas
    print("\n--- Búsquedas ---")
    print("Productos en Hogar:", [p.nombre for p in mp.buscar_productos(categoria=cat_hogar)])
    print("Servicios disponibles:", [s.nombre for s in mp.buscar_servicios()])

    print("\n[OK] Demo completada.")


if __name__ == "__main__":
    main()