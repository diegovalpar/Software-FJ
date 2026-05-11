# custom_exceptions.py
class SoftwareFJError(Exception):
    """Base para errores del sistema Software FJ"""
    pass

class InvalidClientDataError(SoftwareFJError):
    """Error en los datos del cliente"""
    pass

class ServiceUnavailableError(SoftwareFJError):
    """Error cuando el servicio no existe o no hay cupo"""
    pass

class ReservationError(SoftwareFJError):
    """Error en el proceso de creación o cancelación de reservas"""
    pass

class InvalidPaymentMethodError(SoftwareFJError):
    """Error en el método de pago"""
    pass