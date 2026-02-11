class DomainError(Exception):
    pass

class ValidationError(DomainError):
    pass

class PermissionError(DomainError):
    pass
