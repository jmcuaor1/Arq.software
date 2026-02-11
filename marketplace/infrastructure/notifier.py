from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify_listing_created(self, phone, title):
        pass

class ConsoleNotifier(Notifier):
    def notify_listing_created(self, phone, title):
        print(f"[NOTIFY] {phone} -> Publicación creada: {title}")
