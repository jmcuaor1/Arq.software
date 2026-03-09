import sys
sys.path.insert(0, 'd:\\VecinoMarket\\Arq.software')

from marketplace.application.services import (
    UsuarioService,
    CategoriaService,
    PublicacionService,
    ServicioService,
    ConsultaService,
    CrearUsuarioCommand,
    CrearCategoriaCommand,
    PublicarProductoCommand,
    PublicarServicioCommand,
    RegistrarConsultaCommand
)
from marketplace.infrastructure.repositories import (
    InMemoryUsuarioRepository,
    InMemoryCategoriaRepository,
    InMemoryProductoRepository,
    InMemoryServicioRepository,
    InMemoryConsultaRepository
)

def main():
    print("=" * 80)
    print("DEMO - COMPONENTES SPRINT 1 (ALCANCE AJUSTADO: CONTACTO)")
    print("=" * 80)
    
    usuario_repo = InMemoryUsuarioRepository() #Inicializar repositorios
    categoria_repo = InMemoryCategoriaRepository()
    producto_repo = InMemoryProductoRepository()
    servicio_repo = InMemoryServicioRepository()
    consulta_repo = InMemoryConsultaRepository()
    
    usuario_service = UsuarioService(usuario_repo)    #Inicializar servicios
    categoria_service = CategoriaService(categoria_repo)
    publicacion_service = PublicacionService(producto_repo, usuario_repo, categoria_repo)
    servicio_service = ServicioService(servicio_repo, usuario_repo, categoria_repo)
    consulta_service = ConsultaService(consulta_repo, usuario_repo, producto_repo, servicio_repo)
    
    print("\n1. CREANDO USUARIOS")  #Crear usuarios
    print("-" * 80)
    
    vendedor = usuario_service.crear_usuario(CrearUsuarioCommand(
        id="user-001",
        nombre="Juan Perez",
        email="juan@example.com",
        telefono="3001112233",
        apartamento="101"
    ))
    print(f"[OK] Vendedor creado: {vendedor.nombre} ({vendedor.email})")
    
    comprador = usuario_service.crear_usuario(CrearUsuarioCommand(
        id="user-002",
        nombre="Maria Garcia",
        email="maria@example.com",
        telefono="3004445566",
        apartamento="202"
    ))
    print(f"[OK] Comprador creado: {comprador.nombre} ({comprador.email})")
    
    print("\n2. CREANDO CATEGORIAS")  #Crear categorias
    print("-" * 80)
    
    cat_productos = categoria_service.crear_categoria(CrearCategoriaCommand(
        id="cat-001",
        nombre="Electronica",
        descripcion="Productos electronicos y tecnologia"
    ))
    print(f"[OK] Categoria creada: {cat_productos.nombre}")
    
    cat_servicios = categoria_service.crear_categoria(CrearCategoriaCommand(
        id="cat-002",
        nombre="Servicios del Hogar",
        descripcion="Servicios de mantenimiento y reparacion"
    ))
    print(f"[OK] Categoria creada: {cat_servicios.nombre}")
    
    print("\n3. PUBLICANDO PRODUCTO")   #Publicar producto
    print("-" * 80)
    
    producto = publicacion_service.publicar_producto(PublicarProductoCommand(
        vendedor_id="user-001",
        vendedor_status="APPROVED",
        nombre="Laptop Dell XPS 13",
        descripcion="Laptop en excelente estado, poco uso",
        precio_cop=2500000,
        categoria_id="cat-001",
        imagenes=["https://example.com/laptop1.jpg"]
    ))
    print(f"[OK] Producto publicado: {producto.nombre} - ${producto.precio:,.0f}")
    
    print("\n4. PUBLICANDO SERVICIO")  #Publicar servicio
    print("-" * 80)
    
    servicio = servicio_service.publicar_servicio(PublicarServicioCommand(
        proveedor_id="user-001",
        proveedor_status="APPROVED",
        nombre="Reparacion de electrodomesticos",
        descripcion="Servicio profesional de reparacion de neveras, lavadoras y estufas",
        precio_cop=50000,
        categoria_id="cat-002"
    ))
    print(f"[OK] Servicio publicado: {servicio.nombre} - ${servicio.precio:,.0f}")
    print(f"   Disponible: {servicio.disponible}")
    
    print("\n5. LISTANDO SERVICIOS") #Listar servicios
    print("-" * 80)
    
    servicios = servicio_service.listar_servicios()
    print(f"Total de servicios: {len(servicios)}")
    for s in servicios:
        print(f"  - {s.nombre} (${s.precio:,.0f}) - Proveedor: {s.proveedor.nombre}")
    
    print("\n6. REGISTRANDO CONSULTAS (NUEVO ALCANCE: CONTACTO)") #Registrando consultas (Nuevo alcance)
    print("-" * 80)
    
    consulta_prod = consulta_service.registrar_consulta(RegistrarConsultaCommand(
        comprador_id="user-002",
        item_id=producto.id,
        item_type="producto",
        mensaje="Hola, me interesa la laptop. ¿Aceptas cambios?"
    ))
    print(f"[OK] Consulta registrada para Producto: {consulta_prod.item.nombre}")
    print(f"   Mensaje: {consulta_prod.mensaje}")
    
    consulta_serv = consulta_service.registrar_consulta(RegistrarConsultaCommand(
        comprador_id="user-002",
        item_id=servicio.id,
        item_type="servicio",
        mensaje="¿Cuándo podrías venir a revisar mi lavadora?"
    ))
    print(f"[OK] Consulta registrada para Servicio: {consulta_serv.item.nombre}")
    print(f"   Mensaje: {consulta_serv.mensaje}")
    
    print("\n7. LISTANDO CONSULTAS RECIBIDAS POR VENDEDOR")  #Listar consultas para el vendedor
    print("-" * 80)
    
    consultas_recibidas = consulta_service.listar_consultas_vendedor("user-001")
    print(f"Total consultas para Juan Perez: {len(consultas_recibidas)}")
    for c in consultas_recibidas:
        print(f"  - De: {c.comprador.nombre} sobre '{c.item.nombre}' - [{c.estado.value}]")

    print("\n" + "=" * 80)
    print("[OK] DEMO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print("\nResumen:")
    print(f"  - Usuarios creados: {len(usuario_service.listar_usuarios())}")
    print(f"  - Categorias creadas: {len(categoria_service.listar_categorias())}")
    print(f"  - Productos publicados: {len(publicacion_service.listar_productos())}")
    print(f"  - Servicios publicados: {len(servicio_service.listar_servicios())}")
    print(f"  - Consultas registradas: {len(consulta_service.listar_consultas_vendedor('user-001'))} (NUEVO)")

if __name__ == "__main__":
    main()
