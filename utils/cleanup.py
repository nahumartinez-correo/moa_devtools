"""Rutinas de limpieza para el proyecto."""

import atexit
from pathlib import Path


_REGISTRO_PYC = False


def eliminar_archivos_pyc(base_dir=None):
    """Elimina los archivos .pyc dentro del árbol del proyecto."""
    base_path = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent

    if not base_path.exists():
        return

    for pyc_file in base_path.rglob("*.pyc"):
        try:
            pyc_file.unlink()
        except Exception:
            # Errores silenciosos para no interrumpir el cierre de la aplicación
            pass


def registrar_limpieza_pyc(base_dir=None):
    """Registra la limpieza de archivos .pyc al finalizar la ejecución."""
    global _REGISTRO_PYC
    if _REGISTRO_PYC:
        return

    base_path = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent
    atexit.register(eliminar_archivos_pyc, base_path)
    _REGISTRO_PYC = True
