import os
from .notifier import ConsoleNotifier, FlaskNotifier


class NotifierFactory:
    """
    Factory que selecciona el notificador según la variable de entorno NOTIFIER_BACKEND.
    Permite cambiar entre ConsoleNotifier (desarrollo local) y FlaskNotifier (Docker/producción)
    sin modificar código de negocio.
    """

    @staticmethod
    def create():
        backend = os.environ.get("NOTIFIER_BACKEND", "console")
        if backend == "flask":
            return FlaskNotifier()
        return ConsoleNotifier()
