"""
Módulo session_state
--------------------
Mantiene variables globales de estado compartidas entre los módulos
de MOA DevTools durante la ejecución.
"""

# Variables de control internas
_session_state = {
    "usar_simulador": False,
    "mostrar_datos_tablas": False,
}


# === FUNCIONES DE CONTROL GENERAL ===

def set_usar_simulador(valor: bool):
    """Activa o desactiva el uso de simuladores."""
    _session_state["usar_simulador"] = bool(valor)


def get_usar_simulador() -> bool:
    """Devuelve True si el uso de simuladores está activado."""
    return _session_state["usar_simulador"]


def set_mostrar_datos_tablas(valor: bool):
    """Activa o desactiva la visualización de los registros de tablas."""
    _session_state["mostrar_datos_tablas"] = bool(valor)


def get_mostrar_datos_tablas() -> bool:
    """Devuelve True si se deben mostrar los registros de tablas."""
    return _session_state["mostrar_datos_tablas"]


def resetear_estado():
    """Restaura el estado global a los valores por defecto."""
    _session_state["usar_simulador"] = False
    _session_state["mostrar_datos_tablas"] = False
