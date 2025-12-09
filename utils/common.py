"""Utilidades comunes para menús y presentación en consola."""

import os


def limpiar_consola(titulo="MOA DevTools"):
    """Limpia la pantalla y muestra un encabezado estándar.

    Args:
        titulo (str): Texto central para mostrar en el encabezado.
    """
    os.system("cls")
    print("=" * 70)
    print(f"        {titulo}")
    print("=" * 70, "\n")
