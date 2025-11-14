"""
Módulo de logging simple y centralizado para MOA DevTools.
"""

import os
from datetime import datetime

LOG_PATH = r"C:\logs\moa_devtools.log"

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log(mensaje):
    """Escribe un mensaje con timestamp en el archivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

def log_info(mensaje):
    log(f"[INFO] {mensaje}")

def log_error(mensaje):
    log(f"[ERROR] {mensaje}")
