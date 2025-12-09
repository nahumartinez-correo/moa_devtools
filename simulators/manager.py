"""Gestión de simuladores y ejecución de procesos auxiliares."""

import subprocess
import sys
from pathlib import Path
from typing import List


CODES_DIR = Path(__file__).resolve().parent / "codes"
_simuladores_activos: List[dict] = []


def obtener_simuladores_disponibles():
    """Devuelve una lista ordenada con los simuladores detectados."""
    simuladores = []
    if not CODES_DIR.exists():
        return simuladores

    for ruta in CODES_DIR.iterdir():
        if ruta.is_dir():
            entry_point = ruta / f"{ruta.name}.py"
            if entry_point.exists():
                simuladores.append(ruta.name)

    return sorted(simuladores, key=str.lower)


def _obtener_entrypoint(simulador):
    return CODES_DIR / simulador / f"{simulador}.py"


def iniciar_simulador_sin_parametros(simulador):
    """Inicia un simulador en un proceso separado sin argumentos adicionales."""
    entrypoint = _obtener_entrypoint(simulador)

    if not entrypoint.exists():
        raise FileNotFoundError(f"No se encontró el entrypoint para {simulador}")

    proceso = subprocess.Popen([sys.executable, str(entrypoint)])
    _simuladores_activos.append({"nombre": simulador, "proceso": proceso})
    return proceso


def _detener_proceso_simulador(registro):
    proceso = registro.get("proceso")
    if proceso is None:
        return False

    if proceso.poll() is not None:
        return False

    try:
        proceso.terminate()
        proceso.wait(timeout=5)
    except Exception:
        try:
            proceso.kill()
        except Exception:
            pass

    return True


def detener_todos_los_simuladores():
    """Intenta detener todas las instancias de simuladores en ejecución."""
    detenidos = 0
    for registro in list(_simuladores_activos):
        if _detener_proceso_simulador(registro):
            detenidos += 1

    _simuladores_activos.clear()
    return detenidos
