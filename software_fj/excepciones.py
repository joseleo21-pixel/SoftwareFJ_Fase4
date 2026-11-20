class ErrorSistema(Exception):
    """Excepción base del sistema."""

class DatosInvalidosError(ErrorSistema):
    """Datos que no cumplen las reglas de validación."""

class ServicioNoDisponibleError(ErrorSistema):
    """Servicio no disponible para reservar."""

class ReservaError(ErrorSistema):
    """Error durante la gestión de una reserva."""

class OperacionNoPermitidaError(ErrorSistema):
    """Operación incompatible con el estado actual."""
