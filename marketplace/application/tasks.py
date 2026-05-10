"""
Tareas asíncronas Celery para VecinoMarket.
Estas tareas se ejecutan en background sin bloquear los requests HTTP.
"""
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def enviar_notificacion_async(self, telefono: str, titulo: str):
    """
    Envía una notificación al microservicio Flask de forma asíncrona.
    Reintenta hasta 3 veces ante fallos de red.
    """
    try:
        from marketplace.infrastructure.factories import NotifierFactory
        notifier = NotifierFactory.create()
        notifier.notify_listing_created(telefono, titulo)
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def generar_reporte_diario():
    """
    Genera un reporte diario del marketplace.
    Tarea de fondo que puede ejecutarse con Celery Beat.
    """
    from marketplace.infrastructure.repositories import (
        InMemoryProductoRepository,
        InMemoryServicioRepository,
        InMemoryUsuarioRepository,
    )
    productos = InMemoryProductoRepository().list_all()
    servicios = InMemoryServicioRepository().list_all()
    usuarios = InMemoryUsuarioRepository().list_all()

    reporte = {
        "total_productos": len(productos),
        "total_servicios": len(servicios),
        "total_usuarios": len(usuarios),
    }
    print(f"[Reporte Diario] {reporte}")
    return reporte
