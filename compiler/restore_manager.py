"""
Gestor de restauración de archivos modificados durante el proceso
del compilador de MOA DevTools.

 - Revertir vía SVN los archivos .h modificados.
 - Mostrar progreso en pantalla.
 - Loguear sólo información general (sin detalle por archivo).
"""

import subprocess
import time
from utils.logger import log_info


def revertir_headers(lista_headers):
    """
    Aplica 'svn revert' sólo a los headers modificados.
    Muestra progreso visible en pantalla.
    NO lee la salida del comando para evitar errores de decodificación.
    """

    total = len(lista_headers)

    if total == 0:
        print("No hay headers para revertir.")
        return

    log_info(f"Inicio de revert de headers. Total: {total}")

    print("\nRevirtiendo modificaciones en headers...\n")

    for i, path in enumerate(lista_headers, 1):

        # --- progreso en consola ---
        porcentaje = (i * 100) // total
        print(f"\rProcesando {i}/{total} ({porcentaje}%)...", end="", flush=True)

        # --- ejecución silenciosa (sin captura de salida) ---
        subprocess.run(
            ["svn", "revert", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(0.01)

    print("\nOperación completada.\n")
    log_info(f"Revert finalizado. Headers revertidos: {total}")
