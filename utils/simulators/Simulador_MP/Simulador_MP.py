# --------------------------------------------------------------
# Simulador_MP.py
# Punto de entrada del simulador. Inicia el servidor principal.
# --------------------------------------------------------------

from Simulador_MP_logger import log
from Simulador_MP_server import start_server

if __name__ == "__main__":
    log("Simulador_MP iniciado.")
    start_server()
    log("Simulador_MP finalizado.")
    # Se mantiene la consola abierta hasta que el usuario presione ENTER.
    try:
        input("Presione ENTER para cerrar la aplicación.")
    except KeyboardInterrupt:
        pass
