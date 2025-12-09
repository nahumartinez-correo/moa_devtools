# tests/simulators_manager.py
"""
Módulo para controlar la ejecución de simuladores de prueba.

Lee el archivo "simulators.txt" dentro de la carpeta de setup
de la prueba y levanta los simuladores correspondientes
ubicados en simulators/codes/.
"""

import os
import subprocess
from config import session_state


# ==========================================================
# VARIABLES INTERNAS
# ==========================================================

procesos_simuladores = []


# ==========================================================
# FUNCIONES PRINCIPALES
# ==========================================================

def iniciar_simuladores(nombre_prueba: str):
    """
    Inicia los simuladores definidos en el archivo 'simulators.txt'
    de la prueba, si la opción usar_simulador está activa.
    """
    if not session_state.get_usar_simulador():
        print("⚙️  Omitiendo simuladores (usar_simulador desactivado).")
        return

    ruta_base = os.path.dirname(__file__)
    ruta_setup = os.path.join(ruta_base, "set_up_tests", nombre_prueba)
    ruta_simuladores_txt = os.path.join(ruta_setup, "simulators.txt")

    if not os.path.exists(ruta_simuladores_txt):
        print(f"⚠️  No se encontró el archivo de simuladores para la prueba '{nombre_prueba}'.")
        return

    print(f"⚙️  Leyendo simuladores desde: {ruta_simuladores_txt}")

    with open(ruta_simuladores_txt, "r", encoding="utf-8") as f:
        simuladores = [line.strip() for line in f if line.strip()]

    if not simuladores:
        print("⚠️  El archivo simulators.txt está vacío.")
        return

    for sim_name in simuladores:
        sim_path = os.path.join(ruta_base, "..", "simulators", "codes", f"{sim_name}.py")
        sim_path = os.path.abspath(sim_path)

        if not os.path.exists(sim_path):
            print(f"❌ No se encontró el simulador '{sim_name}' en simulators/codes/")
            continue

        try:
            proceso = subprocess.Popen(["python", sim_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            procesos_simuladores.append(proceso)
            print(f"✅ Simulador '{sim_name}' iniciado correctamente (PID {proceso.pid}).")
        except Exception as e:
            print(f"❌ Error al iniciar el simulador '{sim_name}': {e}")


def detener_simuladores():
    """Detiene todos los simuladores que se hayan iniciado."""
    if not procesos_simuladores:
        print("⚙️  No hay simuladores activos para detener.")
        return

    print("\n🧱 Deteniendo simuladores...")
    for proceso in procesos_simuladores:
        try:
            proceso.terminate()
            proceso.wait(timeout=5)
            print(f"✅ Simulador (PID {proceso.pid}) detenido correctamente.")
        except Exception as e:
            print(f"⚠️  No se pudo detener el simulador (PID {proceso.pid}): {e}")

    procesos_simuladores.clear()
