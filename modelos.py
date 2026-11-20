from abc import ABC, abstractmethod
from datetime import datetime
from .excepciones import (DatosInvalidosError, ServicioNoDisponibleError,
                          ReservaError, OperacionNoPermitidaError)

class Entidad(ABC):
    """Clase abstracta para los objetos identificables del sistema."""
    def __init__(self, identificador, nombre):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("El identificador es obligatorio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")
        self._identificador = identificador.strip()
        self._nombre = nombre.strip()

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def describir(self):
        pass

class Cliente(Entidad):
    """Cliente con correo y teléfono encapsulados y validados."""
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador, nombre)
        self.correo = correo
        self.telefono = telefono

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError("El correo electrónico no es válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        digitos = "".join(c for c in str(valor) if c.isdigit())
        if not 7 <= len(digitos) <= 15:
            raise DatosInvalidosError("El teléfono debe tener entre 7 y 15 dígitos.")
        self._telefono = digitos

    def describir(self):
        return f"Cliente {self.nombre} | {self.correo} | {self.telefono}"

class Servicio(Entidad, ABC):
    """Clase abstracta que define el comportamiento común de los servicios."""
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador, nombre)
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatosInvalidosError("La tarifa debe ser un número positivo.")
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"{self.nombre} no está disponible.")

    @abstractmethod
    def calcular_costo(self, horas, *args, **kwargs):
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

class ReservaSala(Servicio):
    def validar_parametros(self, **kwargs):
        horas = kwargs.get("horas")
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("Las horas de sala deben ser positivas.")

    def calcular_costo(self, horas, *args, **kwargs):
        self.validar_parametros(horas=horas)
        descuento = kwargs.get("descuento", 0)
        impuesto = kwargs.get("impuesto", 0)
        if not 0 <= descuento < 1 or not 0 <= impuesto:
            raise DatosInvalidosError("Descuento o impuesto fuera de rango.")
        return round(self.tarifa_hora * horas * (1-descuento) * (1+impuesto), 2)

    def describir(self):
        return f"Sala {self.nombre} - ${self.tarifa_hora:,.2f}/hora"

class AlquilerEquipo(Servicio):
    def validar_parametros(self, **kwargs):
        horas, cantidad = kwargs.get("horas"), kwargs.get("cantidad", 1)
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("Las horas de alquiler deben ser positivas.")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise DatosInvalidosError("La cantidad debe ser un entero positivo.")

    def calcular_costo(self, horas, *args, **kwargs):
        cantidad = kwargs.get("cantidad", 1)
        self.validar_parametros(horas=horas, cantidad=cantidad)
        descuento, impuesto = kwargs.get("descuento", 0), kwargs.get("impuesto", 0)
        if not 0 <= descuento < 1 or impuesto < 0:
            raise DatosInvalidosError("Descuento o impuesto fuera de rango.")
        return round(self.tarifa_hora * horas * cantidad * (1-descuento) * (1+impuesto), 2)

    def describir(self):
        return f"Equipo {self.nombre} - ${self.tarifa_hora:,.2f}/hora/unidad"

class Asesoria(Servicio):
    def validar_parametros(self, **kwargs):
        horas, especialidad = kwargs.get("horas"), kwargs.get("especialidad")
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Debe indicar el área de asesoría.")

    def calcular_costo(self, horas, *args, **kwargs):
        especialidad = kwargs.get("especialidad", "General")
        self.validar_parametros(horas=horas, especialidad=especialidad)
        recargo, impuesto = kwargs.get("recargo", 0), kwargs.get("impuesto", 0)
        if recargo < 0 or impuesto < 0:
            raise DatosInvalidosError("El recargo y el impuesto no pueden ser negativos.")
        return round(self.tarifa_hora * horas * (1+recargo) * (1+impuesto), 2)

    def describir(self):
        return f"Asesoría {self.nombre} - ${self.tarifa_hora:,.2f}/hora"

class Reserva(Entidad):
    """Relaciona un cliente y un servicio; controla el ciclo de la reserva."""
    def __init__(self, identificador, cliente, servicio, duracion, **opciones):
        super().__init__(identificador, f"Reserva {identificador}")
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Debe asociar un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Debe asociar un servicio válido.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser positiva.")
        servicio.validar_disponibilidad()
        self.cliente, self.servicio = cliente, servicio
        self.duracion, self.opciones = float(duracion), opciones
        self.estado = "PENDIENTE"
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError("Solo se confirma una reserva pendiente.")
        self.servicio.validar_disponibilidad()
        self.estado = "CONFIRMADA"
        return self.estado

    def cancelar(self):
        if self.estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError("No se puede cancelar esta reserva.")
        self.estado = "CANCELADA"
        return self.estado

    def procesar(self, impuesto=0):
        if self.estado != "CONFIRMADA":
            raise ReservaError("La reserva debe estar confirmada para procesarse.")
        try:
            costo = self.servicio.calcular_costo(
                self.duracion, impuesto=impuesto, **self.opciones
            )
        except (TypeError, ValueError) as exc:
            raise ReservaError("No se pudo calcular el costo.") from exc
        if costo <= 0:
            raise ReservaError("El costo calculado no es válido.")
        self.estado = "PROCESADA"
        return costo

    def describir(self):
        return f"{self.identificador}: {self.cliente.nombre} / {self.servicio.nombre} / {self.estado}"
