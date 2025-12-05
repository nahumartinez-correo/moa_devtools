"""Menú base de simuladores para MOA DevTools."""

import os
from utils.menu import mostrar_menu


def _limpiar_consola():
    """Limpia la pantalla y muestra el encabezado del menú de simuladores."""
    os.system("cls")
    print("=" * 70)
    print("        MOA DevTools - SIMULADORES")
    print("=" * 70, "\n")


def menu_simuladores():
    """Presenta el menú de simuladores y sus opciones principales."""
    while True:
        _limpiar_consola()
        opcion = mostrar_menu(
            "SIMULADORES",
            [
                "Iniciar sin parámetros",
                "Iniciar con parámetros",
                "Cerrar todas las instancias",
            ],
        )

        if opcion == 0:
            return
        if opcion == 1:
            _mostrar_pantalla_construccion("Inicio sin parámetros")
        elif opcion == 2:
            _mostrar_menu_parametros()
        elif opcion == 3:
            _mostrar_pantalla_construccion("Cierre de instancias")


def _mostrar_pantalla_construccion(contexto):
    """Muestra la pantalla de construcción para opciones aún no implementadas."""
    _limpiar_consola()
    print(f"=== {contexto.upper()} ===\n")
    print("Pantalla en construcción.\n")
    input("Presione ENTER para volver al menú anterior...")


def _mostrar_menu_parametros():
    """Despliega el submenú de parámetros del simulador."""
    while True:
        _limpiar_consola()
        opcion = mostrar_menu(
            "Parámetros del simulador",
            ["Pantalla en construcción"],
        )

        if opcion == 0:
            return

        print("\nLa configuración de parámetros se encuentra en construcción.\n")
        input("Presione ENTER para volver al menú anterior...")
