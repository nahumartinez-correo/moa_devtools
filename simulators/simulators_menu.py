import os
from utils.menu import mostrar_menu


def limpiar_consola():
    """Limpia la pantalla y muestra el encabezado del módulo de simuladores."""
    os.system("cls")
    print("=" * 70)
    print("        MOA DevTools - SIMULADORES")
    print("=" * 70, "\n")


def _pantalla_en_construccion(titulo_opcion):
    """Muestra un mensaje temporal mientras se desarrolla la funcionalidad."""
    limpiar_consola()
    print(f"=== {titulo_opcion} ===\n")
    print("Pantalla en construcción.\n")
    input("Presione ENTER para volver al menú de simuladores...")


def menu_simuladores():
    """Menú principal de simuladores."""
    while True:
        limpiar_consola()
        opcion = mostrar_menu("MENÚ DE SIMULADORES", [
            "Iniciar sin parámetros",
            "Iniciar con parámetros",
            "Detener todos los simuladores"
        ])

        if opcion == 0:
            print("\n↩️  Volviendo al menú principal...\n")
            return
        elif opcion == 1:
            _pantalla_en_construccion("Iniciar sin parámetros")
        elif opcion == 2:
            _pantalla_en_construccion("Iniciar con parámetros")
        elif opcion == 3:
            _pantalla_en_construccion("Detener todos los simuladores")
