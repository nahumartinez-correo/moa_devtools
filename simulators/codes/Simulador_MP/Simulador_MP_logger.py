# --------------------------------------------------------------
# Simulador_MP_logger.py
# Módulo de logging simple: imprime por consola y escribe a archivo.
# --------------------------------------------------------------

import datetime

LOG_FILE = "Simulador_MP.log"

def log(msg: str) -> None:
    """Registra un mensaje con timestamp en consola y en archivo de log."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line)
    except Exception:
        pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
