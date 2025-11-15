"""
Módulo para obtener archivos modificados según SVN.
Se filtran únicamente archivos dentro de POST,
excluyendo los .h.
"""

import subprocess
import os


def obtener_archivos_modificados(ruta_post):
    """
    Ejecuta 'svn status' en la carpeta POST y devuelve una lista
    de nombres de archivo modificados (excluyendo .h).
    Los archivos de código en Mosaic no tienen extensión.

    Retorna:
        lista de strings con rutas relativas respecto a POST.
    """
    cmd = ["svn", "status", ruta_post]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    salida = result.stdout.strip().splitlines()

    modificados = []
    for linea in salida:
        if not linea:
            continue

        if linea[0] not in {"M", "A", "D", "R"}:
            continue

        partes = linea.split(maxsplit=1)
        if len(partes) != 2:
            continue

        ruta_rel = partes[1].strip()

        # excluir headers
        if ruta_rel.lower().endswith(".h"):
            continue

        # mantener rutas relativas
        modificados.append(ruta_rel.replace("/", "\\"))

    # ordenar por fecha de modificación real
    archivos_con_fechas = []
    for rel in modificados:
        ruta_abs = os.path.join(ruta_post, rel)
        if os.path.exists(ruta_abs):
            mtime = os.path.getmtime(ruta_abs)
            archivos_con_fechas.append((rel, mtime))

    archivos_con_fechas.sort(key=lambda x: x[1], reverse=True)

    return [a[0] for a in archivos_con_fechas]
