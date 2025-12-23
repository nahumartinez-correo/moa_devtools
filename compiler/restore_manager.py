"""
Gestor de restauración de archivos modificados durante el proceso
del compilador de MOA DevTools.

 - Revertir vía VCS los archivos .h modificados.
 - Mostrar progreso en pantalla.
 - Loguear sólo información general (sin detalle por archivo).
"""

import time
from utils.logger import log_info, log_error
from compiler.vcs_backend import get_vcs_backend_for_version


def revertir_headers(lista_headers, version):
    """
    Revierte los headers modificados usando el backend de control de versiones
    correspondiente a la versión actual.
    Muestra progreso visible en pantalla.
    NO lee la salida del comando para evitar errores de decodificación.
    """

    total = len(lista_headers)

    if total == 0:
        print("No hay headers para revertir.")
        return

    log_info(f"Inicio de revert de headers. Total: {total}")

    print("\nRevirtiendo modificaciones en headers...\n")

    try:
        backend = get_vcs_backend_for_version(version)
    except Exception as exc:  # pylint: disable=broad-except
        log_error(f"No se pudo determinar el backend de revert: {exc}")
        print("No fue posible revertir los headers modificados.\n")
        return

    for i, path in enumerate(lista_headers, 1):

        # --- progreso en consola ---
        porcentaje = (i * 100) // total
        # Imprimir solo cuando cambie a un múltiplo de 5
        if porcentaje % 5 == 0:
            print(f"\rProcesando {i}/{total} ({porcentaje}%)...", end="", flush=True)

        try:
            backend.revert_files([path])
        except Exception as exc:  # pylint: disable=broad-except
            log_error(f"Error revirtiendo {path}: {exc}")

        #time.sleep(0.001)

    print("\nOperación completada.\n")
    log_info(f"Revert finalizado. Headers revertidos: {total}")
