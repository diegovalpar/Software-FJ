# Diego Valencia
# Grupo 213023_420
# Fase 4 Componente práctico - Prácticas simuladas
# Ejercicio: Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Software FJ

import abc
import datetime

# Importación de excepciones
from custom_exceptions import *

# Manejo de archivos sin necesidad de usar base de datos.
def registrar_evento(mensaje):
    """ Registra errores y eventos relevantes en un archivo de texto."""
    with open("log_sistema.txt", "a", encoding="utf-8") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] {mensaje}\n")

# Clase abstracta que represente entidades generales del sistema.
class EntidadSistema(abc.ABC):
    """Clase abstracta pura que define la estructura base para entidades del sistema."""
    @abc.abstractmethod
    def mostrar_detalle(self):
        pass

# clase Cliente con validaciones robustas y encapsulación de datos personales.
class Cliente(EntidadSistema):
    """Clase Cliente con validaciones robustas y atributos privados (__)."""
    def __init__(self, nombre, cedula):
        if not nombre or not cedula:
            raise InvalidClientDataError("Error: El nombre y la identificación no pueden estar vacíos.")
        self.__nombre = nombre  # Atributo encapsulado (privado)
        self.__cedula = cedula  # Atributo encapsulado (privado)

    def mostrar_detalle(self):
        """Implementación del método abstracto para retornar información segura."""
        return f"Cliente: {self.__nombre} | ID: {self.__cedula}"

# Clase abstracta Servicio y tres servicios especializados.
class Servicio(abc.ABC):
    """Clase abstracta base para la jerarquía de servicios."""
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_total(self, cantidad):
        pass

class Sala(Servicio):
    def calcular_total(self, horas):
        return self.precio_base * horas

class Equipo(Servicio):
    def calcular_total(self, dias, con_seguro=True):
        subtotal = self.precio_base * dias
        return subtotal + 15 if con_seguro else subtotal

class Asesoria(Servicio):
    def calcular_total(self, sesiones):
        return (self.precio_base * sesiones) * 1.15

# Una clase Reserva que integre cliente, servicio, duración y estado.
class Reserva:
    """Clase que integra Cliente y Servicio con manejo de excepciones."""
    def __init__(self, cliente, servicio, cantidad):
        try:
            if cantidad <= 0:
                raise ReservationError("Error: La cantidad debe ser mayor a cero.")
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = cantidad
            self.estado = "Confirmada" # Atributo de estado que refleja el resultado de la reserva
            self.total = servicio.calcular_total(cantidad)
        except Exception as e:
            registrar_evento(f"Error en Reserva: {e}")
            raise









