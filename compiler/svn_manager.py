"""
Gestor de interacción con SVN para detección de cambios.
"""

import os
import re
import subprocess

def obtener_versiones(carpeta_base):
    """Devuelve las carpetas con formato Vxx.yy, ordenadas numéricamente."""
    versiones = []
    for nombre in os.listdir(carpeta_base):
        if re.match(r"V\d{2}\.\d{2}", nombre):
            versiones.append(nombre)
    versiones.sort(key=lambda v: [int(x) for x in re.findall(r"\d+", v)])
    return versiones


def listar_cambios_svn(ruta_version):
    """Ejecuta 'svn status' y devuelve una lista con rutas relativas modificadas."""
    cmd = ["svn", "status", ruta_version]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    salida = result.stdout.strip().splitlines()

    modificados = []
    for linea in salida:
        if linea and linea[0] in {"M", "A", "D", "R"}:
            partes = linea.split(maxsplit=1)
            if len(partes) == 2:
                modificados.append(partes[1].strip())
    return modificados
