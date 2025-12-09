"""Rutinas de limpieza para el proyecto."""

import atexit
from pathlib import Path


_REGISTRO_PYC = False


def eliminar_compilados_y_caches(base_dir=None):
    """Elimina archivos .pyc y carpetas __pycache__ dentro del proyecto."""
    base_path = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent

    if not base_path.exists():
        return

    for pyc_file in base_path.rglob("*.pyc"):
        try:
            pyc_file.unlink()
        except Exception:
            # Errores silenciosos para no interrumpir el cierre de la aplicación
            pass

    for cache_dir in base_path.rglob("__pycache__"):
        try:
            cache_dir.rmdir()
        except Exception:
            # Si no se puede eliminar, continuar sin interrumpir
            pass


def _detener_simuladores_activos():
    """Intenta detener cualquier simulador que siga en ejecución."""
    try:
        from simulators.manager import detener_todos_los_simuladores

        detener_todos_los_simuladores()
    except Exception:
        # No impedir el cierre por errores al detener simuladores
        pass


def _limpieza_final(base_dir=None):
    _detener_simuladores_activos()
    eliminar_compilados_y_caches(base_dir)


def registrar_limpieza_pyc(base_dir=None):
    """Registra la limpieza de compilados y simuladores al finalizar la ejecución."""
    global _REGISTRO_PYC
    if _REGISTRO_PYC:
        return

    base_path = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent
    atexit.register(_limpieza_final, base_path)
    _REGISTRO_PYC = True
