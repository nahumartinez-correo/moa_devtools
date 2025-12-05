"""Menú de simuladores para MOA DevTools."""

from utils.menu import mostrar_menu


def menu_simuladores():
    while True:
        opcion = mostrar_menu(
            "Simuladores",
            [
                "Iniciar sin parámetros",
                "Iniciar con parámetros",
                "Cerrar todas las instancias",
            ],
        )

        if opcion == 0:
            break
        if opcion == 1:
            print("\nLa opción de inicio sin parámetros se encuentra en construcción.")
            input("\nPresione Enter para continuar...")
        elif opcion == 2:
            _mostrar_menu_parametros()
        elif opcion == 3:
            print("\nEl cierre de instancias se encuentra en construcción.")
            input("\nPresione Enter para continuar...")


def _mostrar_menu_parametros():
    opcion = mostrar_menu(
        "Parámetros del simulador",
        [
            "Pantalla en construcción",
        ],
    )

    if opcion == 0:
        return
    print("\nLa configuración de parámetros se encuentra en construcción.")
    input("\nPresione Enter para continuar...")
