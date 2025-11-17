"""
Módulo para obtener versiones del proyecto MOA ordenadas por fecha
de modificación. Las versiones válidas tienen formato Vxx.xx.
"""

import os
import re


def obtener_versiones_ordenadas(carpeta_base):
    """
    Devuelve una lista de carpetas con formato Vxx.xx,
    ordenadas por fecha de última modificación (más reciente primero).
    """
    versiones = []

    for nombre in os.listdir(carpeta_base):
        if not re.fullmatch(r"V\d{2}\.\d{2}", nombre):
            continue

        ruta = os.path.join(carpeta_base, nombre)
        if os.path.isdir(ruta):
            mtime = os.path.getmtime(ruta)
            versiones.append((nombre, mtime))

    versiones.sort(key=lambda x: x[1], reverse=True)
    return [v[0] for v in versiones]
