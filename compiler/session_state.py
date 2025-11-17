"""
Módulo que mantiene el estado interno de una sesión de compilación.
Se utiliza para recordar la versión seleccionada y la lista de
headers modificados al aplicar patches de includes.
"""


class SessionState:
    """
    Clase simple para mantener el estado de una sesión de compilación.

    Atributos:
        version (str): Versión seleccionada, en formato Vxx.xx.
        modificados_h (list[str]): Lista de rutas absolutas de headers .h
                                   modificados durante el patch inicial.
    """

    def __init__(self):
        self.version = None
        self.modificados_h = []
