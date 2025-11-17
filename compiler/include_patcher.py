"""
Aplica los reemplazos generales definidos en includes_manager
sobre todos los archivos .h de la versión seleccionada.
"""

import os
from utils.logger import log_info, log_error
from compiler.includes_manager import obtener_reemplazos_generales

CARPETA_MOAPROJ = r"C:\moaproj"


def aplicar_patches_generales(version):
    """
    Recorre todos los .h dentro de C:\moaproj\{version}\src\
    y reemplaza las líneas definidas.
    Retorna la lista de archivos modificados.
    """

    ruta_src = os.path.join(CARPETA_MOAPROJ, version, "src")
    reemplazos = obtener_reemplazos_generales(version)

    log_info(f"Aplicación de includes generales iniciada para versión {version}.")
    log_info(f"Total de reemplazos definidos: {len(reemplazos)}")

    modificados = []

    for root, _, files in os.walk(ruta_src):
        count = 0
        for file in files:
            if not file.lower().endswith(".h"):
                continue

            path = os.path.join(root, file)
            if _procesar_archivo(path, reemplazos):
                modificados.append(path)
                count += 1

    log_info(f"Total de headers modificados: {len(modificados)}")
    return modificados


def _procesar_archivo(path, reemplazos):
    """Aplica los reemplazos literales en el archivo indicado."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
    except Exception as e:
        log_error(f"No fue posible leer {path}: {e}")
        return False

    nuevo = contenido
    cambios = 0

    for viejo, nuevo_val in reemplazos.items():
        if viejo in nuevo:
            cambios += nuevo.count(viejo)
        nuevo = nuevo.replace(viejo, nuevo_val)

    if cambios == 0:
        return False

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(nuevo)
        return True
    except Exception as e:
        log_error(f"Error escribiendo archivo {path}: {e}")
        return False
