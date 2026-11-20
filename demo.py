"""Demostración de 16 operaciones completas y fallidas del sistema."""
from software_fj.modelos import Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva
from software_fj.gestor import GestorSistema, logger, LOG_PATH
from software_fj.excepciones import ErrorSistema

def ejecutar(numero, titulo, funcion):
    print(f"\\n[{numero}] {titulo}")
    try:
        resultado = funcion()
    except ErrorSistema as error:
        logger.exception("Error controlado en operación %s", numero)
        print("ERROR CONTROLADO:", error)
    except Exception as error:
        logger.exception("Error inesperado en operación %s", numero)
        print("ERROR INESPERADO:", error)
    else:
        logger.info("Operación %s completada", numero)
        print("OK:", resultado)
    finally:
        print("Fin de operación.")

def main():
    app = GestorSistema()

    ejecutar(1, "Registrar cliente válido", lambda: app.registrar_cliente(
        Cliente("C001", "Laura Gómez", "laura@email.com", "3001234567")).describir())
    ejecutar(2, "Registrar segundo cliente", lambda: app.registrar_cliente(
        Cliente("C002", "Carlos Pérez", "carlos@email.com", "3107654321")).describir())
    ejecutar(3, "Rechazar correo inválido", lambda: app.registrar_cliente(
        Cliente("C003", "Cliente Inválido", "correo-no-valido", "3001234567")))

    sala = ReservaSala("S001", "Sala de reuniones", 50000)
    equipo = AlquilerEquipo("E001", "Computador portátil", 12000)
    asesoria = Asesoria("A001", "Asesoría de software", 80000)
    ejecutar(4, "Registrar sala", lambda: app.registrar_servicio(sala).describir())
    ejecutar(5, "Registrar equipo", lambda: app.registrar_servicio(equipo).describir())
    ejecutar(6, "Registrar asesoría", lambda: app.registrar_servicio(asesoria).describir())
    ejecutar(7, "Rechazar tarifa cero", lambda: ReservaSala("S002", "Sala inválida", 0))

    cliente1, cliente2 = app.buscar_cliente("C001"), app.buscar_cliente("C002")
    r1 = Reserva("R001", cliente1, sala, 2, descuento=0.10)
    ejecutar(8, "Crear reserva de sala", lambda: app.crear_reserva(r1).describir())
    ejecutar(9, "Confirmar reserva", lambda: r1.confirmar())
    ejecutar(10, "Procesar reserva con impuesto del 19%",
             lambda: f"${r1.procesar(impuesto=0.19):,.2f}")
    ejecutar(11, "Impedir reprocesamiento", lambda: r1.procesar())
    ejecutar(12, "Rechazar duración negativa",
             lambda: Reserva("R002", cliente1, equipo, -2, cantidad=2))

    r2 = Reserva("R003", cliente2, equipo, 3, cantidad=2, descuento=0.05)
    def operacion_equipo():
        app.crear_reserva(r2)
        r2.confirmar()
        return f"${r2.procesar(impuesto=0.19):,.2f}"
    ejecutar(13, "Procesar alquiler de dos equipos", operacion_equipo)

    r3 = Reserva("R004", cliente1, asesoria, 1.5,
                 especialidad="Desarrollo de software", recargo=0.10)
    def operacion_asesoria():
        app.crear_reserva(r3)
        r3.confirmar()
        return f"${r3.procesar(impuesto=0.19):,.2f}"
    ejecutar(14, "Procesar asesoría especializada", operacion_asesoria)
    ejecutar(15, "Buscar cliente inexistente", lambda: app.buscar_cliente("C999"))

    servicio_inactivo = ReservaSala("S003", "Sala fuera de servicio", 40000, disponible=False)
    ejecutar(16, "Rechazar reserva de servicio no disponible",
             lambda: Reserva("R005", cliente2, servicio_inactivo, 1))

    print("\\nRESUMEN:", app.resumen())
    print("Logs:", LOG_PATH)

if __name__ == "__main__":
    main()
