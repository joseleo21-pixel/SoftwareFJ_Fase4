import logging
from pathlib import Path
from .modelos import Cliente, Servicio, Reserva
from .excepciones import DatosInvalidosError

LOG_PATH = Path(__file__).resolve().parent.parent / "software_fj.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    encoding="utf-8")
logger = logging.getLogger("SoftwareFJ")

class GestorSistema:
    """Administra los objetos en listas; no utiliza base de datos."""
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []

    def _registrar(self, objeto, lista, tipo):
        if not isinstance(objeto, tipo):
            raise DatosInvalidosError(f"El objeto no corresponde a {tipo.__name__}.")
        if any(x.identificador == objeto.identificador for x in lista):
            raise DatosInvalidosError("Ya existe un registro con ese identificador.")
        lista.append(objeto)
        logger.info("Registro creado: %s", objeto.identificador)
        return objeto

    def registrar_cliente(self, cliente):
        return self._registrar(cliente, self.clientes, Cliente)

    def registrar_servicio(self, servicio):
        return self._registrar(servicio, self.servicios, Servicio)

    def crear_reserva(self, reserva):
        return self._registrar(reserva, self.reservas, Reserva)

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        raise DatosInvalidosError(f"No existe el cliente {identificador}.")

    def resumen(self):
        return {"clientes": len(self.clientes),
                "servicios": len(self.servicios),
                "reservas": len(self.reservas)}
