"""
Ejecución de scripts de sucursal y operador.
"""

import subprocess

from config.constants import ENV, SUCURSAL, RUTA_INIT_SUC, RUTA_OPER_TEST
from utils.logger import log_info, log_error


def ejecutar_initsuc():
    print("Ejecutando InitSuc...")
    return _ejecutar_comando(
        ["cmd", "/c", "InitSuc.bat", ENV, SUCURSAL],
        "InitSuc",
        cwd=RUTA_INIT_SUC,
    )


def ejecutar_oper_test():
    print("Ejecutando oper_test...")
    return _ejecutar_comando(
        ["perl", "oper_test.pl", ENV, SUCURSAL],
        "oper_test",
        cwd=RUTA_OPER_TEST,
    )


def _ejecutar_comando(cmd, descripcion, cwd=None):
    log_info(f"Ejecutando comando: {descripcion}")
    resultado = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if resultado.returncode != 0:
        log_error(
            f"Comando falló ({descripcion}). STDOUT: {resultado.stdout} "
            f"STDERR: {resultado.stderr}"
        )
        return False
    if resultado.stdout:
        log_info(f"{descripcion} STDOUT: {resultado.stdout.strip()}")
    if resultado.stderr:
        log_error(f"{descripcion} STDERR: {resultado.stderr.strip()}")
    return True
