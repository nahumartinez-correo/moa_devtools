from utils.common import limpiar_consola
from utils.menu import mostrar_menu
from simulators.manager import (
    obtener_simuladores_disponibles,
    iniciar_simulador_sin_parametros,
    iniciar_simulador_con_condicion,
    obtener_condiciones_simulador,
    detener_todos_los_simuladores,
)


ENCABEZADO_SIMULADORES = "MOA DevTools - SIMULADORES"


def _pantalla_en_construccion(titulo_opcion, simulador=None, modo=None):
    """Muestra un mensaje temporal mientras se desarrolla la funcionalidad."""
    limpiar_consola(ENCABEZADO_SIMULADORES)
    print(f"=== {titulo_opcion} ===\n")

    mensaje_modo = f" (modo: {modo})" if modo else ""
    mensaje_simulador = f" para {simulador}" if simulador else ""
    print(f"Pantalla en construcción{mensaje_simulador}{mensaje_modo}.\n")
    input("Presione ENTER para volver...")


def _menu_selector_simulador(modo: str, interactivo: bool = False):
    """Permite seleccionar un simulador según el modo solicitado."""
    while True:
        simuladores = obtener_simuladores_disponibles()
        limpiar_consola(ENCABEZADO_SIMULADORES)

        if not simuladores:
            print("⚠️  No se encontraron simuladores disponibles.\n")
            input("Presione ENTER para volver...")
            return

        opcion = mostrar_menu("SELECCIONE UN SIMULADOR", simuladores)

        if opcion == 0:
            return

        simulador_elegido = simuladores[opcion - 1]
        if modo == "sin_parametros":
            try:
                proceso = iniciar_simulador_sin_parametros(
                    simulador_elegido, interactivo=interactivo
                )
                modo_texto = "sin parámetros"
                if interactivo:
                    modo_texto += " (modo interactivo)"
                print(
                    f"🚀 Simulador '{simulador_elegido}' iniciado {modo_texto} (PID {proceso.pid}).\n"
                )
            except FileNotFoundError as e:
                print(f"❌ No se pudo iniciar el simulador: {e}\n")
            except Exception as e:
                print(f"❌ Error inesperado al iniciar el simulador: {e}\n")

            input("Presione ENTER para volver al menú de simuladores...")
        else:
            _menu_selector_condicion(simulador_elegido, interactivo)


def _formatear_nombre_condicion(nombre_clave):
    return nombre_clave.replace("_", " ").capitalize()


def _menu_selector_condicion(simulador, interactivo: bool = False):
    """Muestra las condiciones disponibles para un simulador y permite ejecutarlo."""
    while True:
        condiciones = obtener_condiciones_simulador(simulador)
        limpiar_consola(ENCABEZADO_SIMULADORES)

        if not condiciones:
            print("⚠️  No hay condiciones definidas para este simulador.\n")
            input("Presione ENTER para volver al menú anterior...")
            return

        opciones = [_formatear_nombre_condicion(nombre) for nombre in condiciones.keys()]
        opcion = mostrar_menu(
            f"CONDICIONES DISPONIBLES - {simulador}",
            opciones,
        )

        if opcion == 0:
            return

        condicion_clave = list(condiciones.keys())[opcion - 1]
        try:
            proceso = iniciar_simulador_con_condicion(
                simulador, condicion_clave, interactivo=interactivo
            )
            modo_texto = "con condición"
            if interactivo:
                modo_texto += " (modo interactivo)"
            print(
                f"🚀 Simulador '{simulador}' iniciado {modo_texto} '{condicion_clave}' (PID {proceso.pid}).\n"
            )
        except FileNotFoundError as e:
            print(f"❌ No se pudo iniciar el simulador: {e}\n")
        except Exception as e:
            print(f"❌ Error inesperado al iniciar el simulador: {e}\n")

        input("Presione ENTER para volver al menú de simuladores...")


def menu_simuladores():
    """Menú principal de simuladores."""
    while True:
        limpiar_consola(ENCABEZADO_SIMULADORES)
        opcion = mostrar_menu("MENÚ DE SIMULADORES", [
            "Iniciar sin parámetros",
            "Iniciar sin parámetros (MODO INTERACTIVO)",
            "Iniciar con parámetros",
            "Iniciar con parámetros (MODO INTERACTIVO)",
            "Detener todos los simuladores"
        ])

        if opcion == 0:
            print("\n↩️  Volviendo al menú principal...\n")
            return
        elif opcion == 1:
            _menu_selector_simulador("sin_parametros")
        elif opcion == 2:
            _menu_selector_simulador("sin_parametros", interactivo=True)
        elif opcion == 3:
            _menu_selector_simulador("con_parametros")
        elif opcion == 4:
            _menu_selector_simulador("con_parametros", interactivo=True)
        elif opcion == 5:
            detener_todos_los_simuladores()
            print("✅ Todos los simuladores han sido detenidos (si había en ejecución).\n")
            input("Presione ENTER para continuar...")
