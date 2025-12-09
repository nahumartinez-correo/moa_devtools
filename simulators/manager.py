"""Gestión de simuladores y ejecución de procesos auxiliares."""

import os
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


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

    proceso = _abrir_proceso_en_consola(entrypoint)
    _simuladores_activos.append({"nombre": simulador, "proceso": proceso})
    return proceso


def iniciar_simulador_con_condicion(simulador: str, condicion: str):
    """Inicia un simulador con una condición específica."""
    entrypoint = _obtener_entrypoint(simulador)

    if not entrypoint.exists():
        raise FileNotFoundError(f"No se encontró el entrypoint para {simulador}")

    proceso = _abrir_proceso_en_consola(entrypoint, ["--condicion", condicion])
    _simuladores_activos.append(
        {"nombre": simulador, "proceso": proceso, "condicion": condicion}
    )
    return proceso


def obtener_condiciones_simulador(simulador: str) -> Dict[str, dict]:
    """Carga dinámicamente las condiciones de un simulador."""
    conditions_path = CODES_DIR / simulador / f"{simulador}_conditions.py"

    if not conditions_path.exists():
        return {}

    spec = importlib.util.spec_from_file_location(
        f"{simulador}_conditions_module", conditions_path
    )
    if spec is None or spec.loader is None:
        return {}

    modulo = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(modulo)
    except Exception:
        return {}

    conditions = getattr(modulo, "CONDITIONS", {})
    return conditions if isinstance(conditions, dict) else {}


def _abrir_proceso_en_consola(entrypoint: Path, extra_args=None):
    """Abre el simulador en una nueva consola cuando es posible."""
    extra_args = extra_args or []
    args = [sys.executable, str(entrypoint)] + list(extra_args)
    popen_kwargs = {}

    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
    else:
        terminal = _terminal_disponible()
        if terminal:
            args = [terminal, "-e", sys.executable, str(entrypoint)] + list(extra_args)
        else:
            popen_kwargs["start_new_session"] = True
            popen_kwargs["stdout"] = subprocess.DEVNULL
            popen_kwargs["stderr"] = subprocess.DEVNULL

    return subprocess.Popen(args, **popen_kwargs)


def _terminal_disponible():
    """Devuelve una terminal gráfica/disponible en sistemas tipo Unix."""
    posibles = [
        "x-terminal-emulator",
        "gnome-terminal",
        "konsole",
        "xfce4-terminal",
        "xterm",
    ]

    for terminal in posibles:
        if shutil.which(terminal):
            return terminal

    return None


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
