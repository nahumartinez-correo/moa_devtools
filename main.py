"""
Integración del menú de compilador con el programa principal.
"""

import os
from utils.menu import mostrar_menu
from compiler.compiler_menu import menu_compilador
from config import simulator_manager
from tests import ahk_runner


def limpiar_consola():
    """Limpia la pantalla y muestra el encabezado."""
    os.system("cls")
    print("MOA DevTools - Herramientas de desarrollo")
    print("Menú principal\n")


def main():
    while True:
        limpiar_consola()
        opcion = mostrar_menu("Menú principal de MOA DevTools", [
            "Compilador de aplicaciones",
            "Configuración de simuladores",
            "Ejecución de pruebas automáticas"
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


if __name__ == "__main__":
    main()
