# --------------------------------------------------------------
# Simulador_MP.py
# Punto de entrada principal del simulador. Recibe parámetros por
# línea de comandos y lanza el servidor configurado.
# --------------------------------------------------------------

import argparse
from Simulador_MP_logger import log
from Simulador_MP_server import start_server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador MercadoPago ISO8583")
    parser.add_argument("--interactivo", action="store_true",
                        help="Activa modo interactivo (pausa por ENTER)")
    parser.add_argument("--condicion", type=str, default=None,
                        help="Nombre de la condición a simular")

    args = parser.parse_args()

    log("Simulador_MP iniciado.")
    start_server(interactivo=args.interactivo, condicion=args.condicion)
    log("Simulador_MP finalizado.")

    try:
        input("Presione ENTER para cerrar la aplicación.")
    except KeyboardInterrupt:
        pass
