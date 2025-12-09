from pathlib import Path
from utils.common import limpiar_consola
from utils.menu import mostrar_menu


CODES_DIR = Path(__file__).resolve().parent / "codes"
ENCABEZADO_SIMULADORES = "MOA DevTools - SIMULADORES"


def _pantalla_en_construccion(titulo_opcion, simulador=None, modo=None):
    """Muestra un mensaje temporal mientras se desarrolla la funcionalidad."""
    limpiar_consola(ENCABEZADO_SIMULADORES)
    print(f"=== {titulo_opcion} ===\n")

    mensaje_modo = f" (modo: {modo})" if modo else ""
    mensaje_simulador = f" para {simulador}" if simulador else ""
    print(f"Pantalla en construcción{mensaje_simulador}{mensaje_modo}.\n")
    input("Presione ENTER para volver...")


def _obtener_simuladores_disponibles():
    """Devuelve una lista ordenada con los simuladores detectados."""
    simuladores = []
    if not CODES_DIR.exists():
        return simuladores

    for ruta in CODES_DIR.iterdir():
        if ruta.is_dir():
            entry_point = ruta / f"{ruta.name}.py"
            if entry_point.exists():
                simuladores.append(ruta.name)

    return sorted(simuladores, key=str.lower)


def _menu_selector_simulador(modo):
    """Permite seleccionar un simulador según el modo solicitado."""
    while True:
        simuladores = _obtener_simuladores_disponibles()
        limpiar_consola(ENCABEZADO_SIMULADORES)

        if not simuladores:
            print("⚠️  No se encontraron simuladores disponibles.\n")
            input("Presione ENTER para volver...")
            return

        opcion = mostrar_menu("SELECCIONE UN SIMULADOR", simuladores)

        if opcion == 0:
            return

        simulador_elegido = simuladores[opcion - 1]
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
            _pantalla_en_construccion("Detener todos los simuladores")
