from utils.common import limpiar_consola
from utils.menu import mostrar_menu
from simulators.manager import (
    obtener_simuladores_disponibles,
    iniciar_simulador_sin_parametros,
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


def _menu_selector_simulador(modo):
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
        if modo == "sin parámetros":
            try:
                proceso = iniciar_simulador_sin_parametros(simulador_elegido)
                print(
                    f"🚀 Simulador '{simulador_elegido}' iniciado sin parámetros (PID {proceso.pid}).\n"
                )
            except FileNotFoundError as e:
                print(f"❌ No se pudo iniciar el simulador: {e}\n")
            except Exception as e:
                print(f"❌ Error inesperado al iniciar el simulador: {e}\n")

            input("Presione ENTER para volver al menú de simuladores...")
        else:
            _pantalla_en_construccion("Simulador en construcción", simulador_elegido, modo)


def menu_simuladores():
    """Menú principal de simuladores."""
    while True:
        limpiar_consola(ENCABEZADO_SIMULADORES)
        opcion = mostrar_menu("MENÚ DE SIMULADORES", [
            "Iniciar sin parámetros",
            "Iniciar con parámetros",
            "Detener todos los simuladores"
        ])

        if opcion == 0:
            print("\n↩️  Volviendo al menú principal...\n")
            return
        elif opcion == 1:
            _menu_selector_simulador("sin parámetros")
        elif opcion == 2:
            _menu_selector_simulador("con parámetros")
        elif opcion == 3:
            detener_todos_los_simuladores()
            print("✅ Todos los simuladores han sido detenidos (si había en ejecución).\n")
            input("Presione ENTER para continuar...")
