from abc import ABC, abstractmethod
import requests


class Notifier(ABC):
    @abstractmethod
    def notify_listing_created(self, phone, title):
        pass


class ConsoleNotifier(Notifier):
    def notify_listing_created(self, phone, title):
        print(f"[NOTIFY] {phone} -> Publicación creada: {title}")


class FlaskNotifier(Notifier):
    """
    Adapter que delega notificaciones al microservicio Flask.
    Implementa Strangler Pattern: Django llama a Flask en lugar de manejar notificaciones internamente.
    """

    FLASK_URL = "http://flask_service:5000/notificaciones/"
    TIMEOUT = 10

    def notify_listing_created(self, phone, title):
        try:
            payload = {
                "telefono": phone or "0000000000",
                "titulo": title,
                "tipo": "consola",
            }
            response = requests.post(self.FLASK_URL, json=payload, timeout=self.TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Fallback silencioso: la notificación no debe bloquear la publicación
            print(f"[FlaskNotifier] Advertencia — microservicio no disponible: {e}")
