class InMemoryProductoRepository:
    def __init__(self):
        self.db = {}

    def add(self, producto):
        self.db[producto.id] = producto

    def list_all(self):
        return list(self.db.values())
