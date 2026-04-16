import os
import sys

def setup_path():
    """Asegura que el script encuentre el paquete marketplace sin importar desde dónde se llame."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

setup_path()

try:
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
except ImportError as e:
    print(f"❌ Error al importar los módulos: {e}")
    print("Asegúrate de estar ejecutando el script desde la raíz del proyecto.")
    sys.exit(1)

def main():
    print("\n=== EXPLORANDO EL CORAZÓN DE VECINOMARKET ===")
    print("-" * 60)
    print("Vamos a verificar que todo el flujo del Sprint 1 esté funcionando como debe.")
    
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
    
    print("\n👥 Paso 1: Registrando a los primeros vecinos en la plataforma...")
    print("-" * 60)
    
    vendedor = usuario_service.crear_usuario(CrearUsuarioCommand(
        id="user-001",
        nombre="Juan Perez",
        email="juan@example.com",
        telefono="3001112233",
        apartamento="101"
    ))
    print(f"✨ ¡Genial! Ya tenemos a {vendedor.nombre} listo para vender.")
    
    comprador = usuario_service.crear_usuario(CrearUsuarioCommand(
        id="user-002",
        nombre="Maria Garcia",
        email="maria@example.com",
        telefono="3004445566",
        apartamento="202"
    ))
    print(f"✨ Y por aquí tenemos a {comprador.nombre} buscando cositas.")
    
    print("\n📂 Paso 2: Organizando el mercado con algunas categorías...")
    print("-" * 60)
    
    cat_productos = categoria_service.crear_categoria(CrearCategoriaCommand(
        id="cat-001",
        nombre="Electronica",
        descripcion="Productos electronicos y tecnologia"
    ))
    print(f"✅ Categoría '{cat_productos.nombre}' activada.")
    
    cat_servicios = categoria_service.crear_categoria(CrearCategoriaCommand(
        id="cat-002",
        nombre="Servicios del Hogar",
        descripcion="Servicios de mantenimiento y reparacion"
    ))
    print(f"✅ Categoría '{cat_servicios.nombre}' activada.")
    
    print("\n📦 Paso 3: Subiendo el primer producto al catálogo...")
    print("-" * 60)
    
    producto = publicacion_service.publicar_producto(PublicarProductoCommand(
        vendedor_id="user-001",
        vendedor_status="APPROVED",
        nombre="Laptop Dell XPS 13",
        descripcion="Laptop en excelente estado, poco uso",
        precio_cop=2500000,
        categoria_id="cat-001",
        imagenes=["https://example.com/laptop1.jpg"]
    ))
    print(f"🔥 ¡Producto arriba! {producto.nombre} por solo ${producto.precio:,.0f}")
    
    print("\n🛠️  Paso 4: Registrando un nuevo servicio en la comunidad...")
    print("-" * 60)
    
    servicio = servicio_service.publicar_servicio(PublicarServicioCommand(
        proveedor_id="user-001",
        proveedor_status="APPROVED",
        nombre="Reparacion de electrodomesticos",
        descripcion="Servicio profesional de reparacion de neveras, lavadoras y estufas",
        precio_cop=50000,
        categoria_id="cat-002"
    ))
    print(f"✅ Servicio de '{servicio.nombre}' publicado correctamente.")
    print(f"   Disponible: {servicio.disponible}")
    
    print("\n🔍 Paso 5: Echando un vistazo a los servicios disponibles...")
    print("-" * 60)
    
    servicios = servicio_service.listar_servicios()
    print(f"Ahora mismo hay {len(servicios)} servicios activos:")
    for s in servicios:
        print(f"  - {s.nombre} (${s.precio:,.0f}) - Proveedor: {s.proveedor.nombre}")
    
    print("\n💬 Paso 6: Probando el sistema de mensajes entre vecinos...")
    print("-" * 60)
    
    consulta_prod = consulta_service.registrar_consulta(RegistrarConsultaCommand(
        comprador_id="user-002",
        item_id=producto.id,
        item_type="producto",
        mensaje="Hola, me interesa la laptop. ¿Aceptas cambios?"
    ))
    print(f"Mensaje enviado sobre: {consulta_prod.item.nombre}")
    print(f"   Dice: \"{consulta_prod.mensaje}\"")
    
    consulta_serv = consulta_service.registrar_consulta(RegistrarConsultaCommand(
        comprador_id="user-002",
        item_id=servicio.id,
        item_type="servicio",
        mensaje="¿Cuándo podrías venir a revisar mi lavadora?"
    ))
    print(f"Consulta enviada por el servicio: {consulta_serv.item.nombre}")
    print(f"   Dice: \"{consulta_serv.mensaje}\"")
    
    print("\n📈 Paso 7: Revisando la bandeja de entrada del vendedor...")
    print("-" * 60)
    
    consultas_recibidas = consulta_service.listar_consultas_vendedor("user-001")
    print(f"Juan Pérez tiene {len(consultas_recibidas)} mensajes nuevos:")
    for c in consultas_recibidas:
        print(f"  - De: {c.comprador.nombre} sobre '{c.item.nombre}' - [{c.estado.value}]")

    print("\n--- PRUEBA COMPLETADA ---")
    print("Todo parece estar funcionando de maravilla. ¡Buen trabajo!")
    print("-" * 60)
    print("\n📊 RESUMEN DE LA OPERACIÓN:")
    print(f"{'Componente':<25} | {'Cantidad':<10}")
    print("-" * 40)
    print(f"{'Usuarios':<25} | {len(usuario_service.listar_usuarios()):<10}")
    print(f"{'Categorias':<25} | {len(categoria_service.listar_categorias()):<10}")
    print(f"{'Productos':<25} | {len(publicacion_service.listar_productos()):<10}")
    print(f"{'Servicios':<25} | {len(servicio_service.listar_servicios()):<10}")
    print(f"{'Consultas':<25} | {len(consulta_service.listar_consultas_vendedor('user-001')):<10}")

if __name__ == "__main__":
    main()
