"""
Módulo principal de MOA DevTools.

Este script es el punto de entrada de la herramienta.
Ofrece un menú principal con las tres funciones básicas:
    1. Compilador
    2. Configuración
    3. Pruebas automáticas
"""

import os
from utils.menu import mostrar_menu
from compiler import builder
from config import simulator_manager
from tests import ahk_runner


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
            "Pruebas automáticas"
        ])

        if opcion == 0:
            print("\nSaliendo de MOA DevTools...")
            break
        elif opcion == 1:
            builder.menu_compilador()
        elif opcion == 2:
            simulator_manager.menu_configuracion()
        elif opcion == 3:
            ahk_runner.menu_pruebas()
        else:
            print("\n⚠️  Opción inválida. Intente nuevamente.")
            input("\nPresione ENTER para continuar...")


if __name__ == "__main__":
    main()
