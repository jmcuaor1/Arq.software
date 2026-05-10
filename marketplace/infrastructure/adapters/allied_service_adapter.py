"""
Adapter para consumir el servicio del equipo aliado.
Implementa fallback graceful si el servicio no está disponible.
"""
import os
import requests


class AlliedServiceAdapter:
    """
    Cliente HTTP para el endpoint del equipo aliado.
    URL configurable vía variable de entorno ALLIED_SERVICE_URL.
    """

    TIMEOUT = 8

    def __init__(self):
        self.base_url = os.environ.get(
            "ALLIED_SERVICE_URL",
            "http://allied-service:8001/api/"
        )

    def get_datos_aliado(self) -> dict:
        """
        Consume el endpoint del equipo aliado.
        Retorna los datos o un objeto con disponible=False si hay error.
        """
        try:
            url = self.base_url.rstrip("/") + "/"
            response = requests.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return {
                "disponible": True,
                "datos": response.json(),
            }
        except requests.exceptions.RequestException as e:
            print(f"[AlliedServiceAdapter] Servicio aliado no disponible: {e}")
            return {
                "disponible": False,
                "datos": [],
                "mensaje": "El servicio aliado no está disponible en este momento.",
            }
