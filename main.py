"""Sistema interactivo Software FJ. Ejecutar con: python main.py"""
from software_fj.modelos import Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva
from software_fj.gestor import GestorSistema, logger, LOG_PATH
from software_fj.excepciones import ErrorSistema


def pedir_texto(mensaje):
    """Solicita un texto obligatorio y evita entradas vacías."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El dato es obligatorio. Inténtalo nuevamente.")


def pedir_numero(mensaje, entero=False):
    """Convierte una entrada numérica y controla errores de digitación."""
    while True:
        try:
            valor = input(mensaje).strip()
            numero = int(valor) if entero else float(valor)
            if numero <= 0:
                print("El valor debe ser mayor que cero.")
                continue
            return numero
        except ValueError as error:
            logger.exception("El usuario ingresó un número inválido")
            print("Debes escribir un número válido. Inténtalo nuevamente.")
            # Encadenamiento de excepciones: la causa queda registrada en el log.
            if not valor:
                logger.error("Entrada numérica vacía: %s", error)


def mostrar_clientes(app):
    if not app.clientes:
        print("Todavía no hay clientes registrados.")
        return
    print("\n--- CLIENTES ---")
    for cliente in app.clientes:
        print(f"{cliente.identificador} | {cliente.nombre} | {cliente.correo} | {cliente.telefono}")


def mostrar_servicios(app):
    if not app.servicios:
        print("Todavía no hay servicios registrados.")
        return
    print("\n--- SERVICIOS ---")
    for servicio in app.servicios:
        estado = "Disponible" if servicio.disponible else "No disponible"
        print(f"{servicio.identificador} | {servicio.describir()} | {estado}")


def mostrar_reservas(app):
    if not app.reservas:
        print("Todavía no hay reservas registradas.")
        return
    print("\n--- RESERVAS ---")
    for reserva in app.reservas:
        print(f"{reserva.identificador} | {reserva.cliente.nombre} | "
              f"{reserva.servicio.nombre} | {reserva.duracion:g} horas | {reserva.estado}")


def registrar_cliente(app):
    print("\nREGISTRO DE CLIENTE")
    identificador = pedir_texto("Identificación o código del cliente: ")
    nombre = pedir_texto("Nombre completo: ")
    correo = pedir_texto("Correo electrónico: ")
    telefono = pedir_texto("Teléfono: ")
    cliente = Cliente(identificador, nombre, correo, telefono)
    app.registrar_cliente(cliente)
    print("Cliente registrado correctamente:", cliente.describir())


def registrar_servicio(app):
    print("\nTIPO DE SERVICIO\n1. Reserva de sala\n2. Alquiler de equipo\n3. Asesoría especializada")
    tipo = pedir_texto("Selecciona una opción: ")
    identificador = pedir_texto("Código del servicio: ")
    nombre = pedir_texto("Nombre o descripción: ")
    tarifa = pedir_numero("Tarifa por hora (COP): ")
    if tipo == "1":
        servicio = ReservaSala(identificador, nombre, tarifa)
    elif tipo == "2":
        servicio = AlquilerEquipo(identificador, nombre, tarifa)
    elif tipo == "3":
        servicio = Asesoria(identificador, nombre, tarifa)
    else:
        raise ErrorSistema("Tipo de servicio no válido. Elige 1, 2 o 3.")
    app.registrar_servicio(servicio)
    print("Servicio registrado correctamente:", servicio.describir())


def crear_reserva(app):
    print("\nCREAR RESERVA")
    mostrar_clientes(app)
    cliente = app.buscar_cliente(pedir_texto("Código del cliente: "))
    mostrar_servicios(app)
    codigo = pedir_texto("Código del servicio: ")
    servicio = next((s for s in app.servicios if s.identificador == codigo), None)
    if servicio is None:
        raise ErrorSistema(f"No existe el servicio {codigo}.")
    duracion = pedir_numero("Duración en horas: ")
    opciones = {}
    if isinstance(servicio, AlquilerEquipo):
        opciones["cantidad"] = pedir_numero("Cantidad de equipos: ", entero=True)
    elif isinstance(servicio, Asesoria):
        opciones["especialidad"] = pedir_texto("Área de asesoría: ")
    identificador = pedir_texto("Código único de la reserva: ")
    reserva = Reserva(identificador, cliente, servicio, duracion, **opciones)
    app.crear_reserva(reserva)
    print("Reserva creada. Estado:", reserva.estado)


def gestionar_reserva(app):
    mostrar_reservas(app)
    codigo = pedir_texto("Código de la reserva: ")
    reserva = next((r for r in app.reservas if r.identificador == codigo), None)
    if reserva is None:
        raise ErrorSistema(f"No existe la reserva {codigo}.")
    print("1. Confirmar\n2. Cancelar\n3. Procesar y calcular costo")
    opcion = pedir_texto("Selecciona una acción: ")
    if opcion == "1":
        print("Reserva:", reserva.confirmar())
    elif opcion == "2":
        print("Reserva:", reserva.cancelar())
    elif opcion == "3":
        impuesto = input("Impuesto (por ejemplo 0.19 para 19%; Enter para 0): ").strip()
        impuesto = float(impuesto) if impuesto else 0
        costo = reserva.procesar(impuesto=impuesto)
        print(f"Reserva procesada. Total: ${costo:,.2f} COP")
    else:
        raise ErrorSistema("Acción no válida.")


def ejecutar_demo(app):
    """Ejecuta operaciones automáticas de demostración solicitadas en el anexo."""
    print("\nLa demostración automática se conserva en la versión inicial del proyecto.")
    print("Para repetirla, revisa el archivo salida_prueba.txt y los registros del log.")
    print("En esta versión los registros reales se hacen desde el menú interactivo.")


def main():
    app = GestorSistema()
    print("=" * 55)
    print("       SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 55)
    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Gestionar reserva (confirmar, cancelar o procesar)")
        print("5. Consultar clientes")
        print("6. Consultar servicios")
        print("7. Consultar reservas")
        print("8. Ver resumen del sistema")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()
        try:
            if opcion == "1":
                registrar_cliente(app)
            elif opcion == "2":
                registrar_servicio(app)
            elif opcion == "3":
                crear_reserva(app)
            elif opcion == "4":
                gestionar_reserva(app)
            elif opcion == "5":
                mostrar_clientes(app)
            elif opcion == "6":
                mostrar_servicios(app)
            elif opcion == "7":
                mostrar_reservas(app)
            elif opcion == "8":
                print("Resumen:", app.resumen())
            elif opcion == "0":
                print("Gracias por utilizar Software FJ.")
                break
            else:
                raise ErrorSistema("Opción incorrecta. Selecciona una opción del menú.")
        except (ErrorSistema, ValueError, TypeError) as error:
            logger.exception("Operación interactiva fallida")
            print("No se pudo completar la operación:", error)
            print("El sistema continúa funcionando. Puedes intentarlo otra vez.")
        except Exception as error:
            logger.exception("Error inesperado en el menú")
            print("Ocurrió un error inesperado:", error)
            print("El error quedó registrado y el sistema sigue activo.")
        else:
            logger.info("Opción del menú ejecutada: %s", opcion)
        finally:
            print("\n--- Fin de la operación ---")
    print("Los eventos y errores se guardaron en:", LOG_PATH)


if __name__ == "__main__":
    main()
