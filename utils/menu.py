"""
Gestor de menús interactivos de consola para MOA DevTools.
Permite definir menús numerados que incluyan la opción 0 para volver o salir.
"""

def mostrar_menu(titulo, opciones, incluir_salida=True):
    """
    Muestra un menú numerado y devuelve el número seleccionado.

    Parámetros:
        titulo (str): Título del menú a mostrar.
        opciones (list[str]): Lista de opciones disponibles.
        incluir_salida (bool): Si es True, agrega la opción "0) Volver o salir".
                               Si es False, se asume que la opción 0 ya está incluida.

    Retorna:
        int: El número de opción elegido por el usuario.
             (0 representa la opción de volver o salir)
    """
    print(f"\n{titulo}\n")

    # Mostrar la opción 0 automáticamente, si corresponde
    if incluir_salida:
        print("0) Volver o salir")

    # Listar las demás opciones
    for i, op in enumerate(opciones, 1):
        print(f"{i}) {op}")

    while True:
        try:
            sel = int(input("\nSeleccione una opción: "))

            # Validación flexible para incluir o no el 0 automático
            if incluir_salida:
                if 0 <= sel <= len(opciones):
                    return sel
            else:
                # Si la opción 0 ya está incluida manualmente en la lista
                if 0 <= sel < len(opciones):
                    return sel

        except ValueError:
            pass

        print("Opción inválida, intente nuevamente.")
