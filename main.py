"""
Integración del menú de compilador con el programa principal.
"""

import os
from utils.menu import mostrar_menu
from compiler.compiler_menu import menu_compilador
from config import simulator_manager
from tests import ahk_runner
from simulators.simulators_menu import menu_simuladores


def limpiar_consola():
    """Limpia la pantalla y muestra el encabezado."""
    os.system("cls")
    print("=" * 70)
    print("        MOA DevTools - HERRAMIENTAS DE DESARROLLO")
    print("=" * 70, "\n")


def main():
    while True:
        limpiar_consola()
        opcion = mostrar_menu("MENÚ PRINCIPAL - MOA DevTools", [
            "Compilador",
            "Configuración",
            "Pruebas automáticas",
            "Simuladores"
        ])

        if opcion == 0:
            print("\nSaliendo de MOA DevTools...")
            break
        elif opcion == 1:
            menu_compilador()
        elif opcion == 2:
            simulator_manager.menu_configuracion()
        elif opcion == 3:
            ahk_runner.menu_pruebas()
        elif opcion == 4:
            menu_simuladores()


if __name__ == "__main__":
    main()
