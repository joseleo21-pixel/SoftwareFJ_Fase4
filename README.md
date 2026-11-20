# Sistema Integral de Gestión - Software FJ

Proyecto académico en Python para gestionar clientes, servicios y reservas sin utilizar bases de datos. La información vive en listas y objetos durante la ejecución; los eventos y errores se registran en `software_fj.log`.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar librerías externas.

## Cómo ejecutar
Abre una terminal en esta carpeta y ejecuta:

```bash
python main.py
```

En Windows también puedes usar `py main.py`. El menú permite registrar clientes, registrar los tres tipos de servicios, crear reservas, confirmarlas, cancelarlas, procesarlas y consultar los registros. Los datos se conservan mientras el programa está abierto; al cerrarlo se reinicia la información porque el enunciado no solicita base de datos.

## Demostración de operaciones
Para ejecutar los casos de prueba automáticos (incluye operaciones correctas e incorrectas y manejo de excepciones), ejecuta:

```bash
python demo.py
```

La salida de una ejecución de demostración está en `salida_prueba.txt`.

## Estructura
- `main.py`: menú interactivo para que el usuario ingrese sus propios datos.
- `demo.py`: demostración automática de operaciones de prueba.
- `software_fj/modelos.py`: entidades, clientes, servicios especializados y reservas.
- `software_fj/excepciones.py`: excepciones personalizadas.
- `software_fj/gestor.py`: administración de listas y configuración de logs.
- `software_fj.log`: registro de eventos y errores (se actualiza al ejecutar el sistema).

## Funcionalidades
- Abstracción mediante clases abstractas `Entidad` y `Servicio`.
- Herencia y polimorfismo en `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- Encapsulación y validación de datos del cliente.
- Reservas con estados pendiente, confirmada, cancelada y procesada.
- Excepciones personalizadas, control `try/except/else/finally` y registro de errores.
- Cálculo de costos con parámetros opcionales para impuestos, descuentos, cantidades y recargos.

## Nota sobre persistencia
Los clientes, servicios y reservas se almacenan en memoria mediante listas. Al cerrar el programa se pierden, tal como corresponde a una simulación sin base de datos. El archivo de logs sí permanece en disco.
