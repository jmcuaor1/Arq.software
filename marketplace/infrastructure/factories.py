from .notifier import ConsoleNotifier

class NotifierFactory:
    @staticmethod
    def create():
        return ConsoleNotifier()
