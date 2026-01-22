"""
Gestor de reemplazo y restauración de includes en headers.
"""

import os

from compiler.includes_manager import obtener_reemplazos_generales
from config.constants import RUTA_GIT_SRC
from utils.logger import log_info, log_error


_HEADERS_BACKUP = {}


def aplicar_includes():
    if _HEADERS_BACKUP:
        log_info("Includes ya aplicados. Se reutiliza el backup existente.")
        return True

    reemplazos = obtener_reemplazos_generales("Mosaic-gitlab")
    if not reemplazos:
        log_error("No se encontraron reemplazos de includes.")
        return False

    for root, _, files in os.walk(RUTA_GIT_SRC):
        for nombre in files:
            if not nombre.lower().endswith(".h"):
                continue
            ruta = os.path.join(root, nombre)
            try:
                with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                    contenido = f.read()
            except Exception as exc:
                log_error(f"No fue posible leer {ruta}: {exc}")
                return False

            nuevo = contenido
            cambios = 0
            for viejo, nuevo_val in reemplazos.items():
                if viejo in nuevo:
                    cambios += nuevo.count(viejo)
                nuevo = nuevo.replace(viejo, nuevo_val)

            if cambios == 0 or nuevo == contenido:
                continue

            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(nuevo)
                _HEADERS_BACKUP[ruta] = contenido
                log_info(f"Header actualizado: {ruta}")
            except Exception as exc:
                log_error(f"No fue posible escribir {ruta}: {exc}")
                return False

    log_info(f"Headers modificados: {len(_HEADERS_BACKUP)}")
    return True


def revertir_includes():
    if not _HEADERS_BACKUP:
        log_info("No hay headers para revertir.")
        return True

    for ruta, contenido in _HEADERS_BACKUP.items():
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            log_info(f"Header restaurado: {ruta}")
        except Exception as exc:
            log_error(f"No se pudo restaurar {ruta}: {exc}")
            return False

    _HEADERS_BACKUP.clear()
    return True
