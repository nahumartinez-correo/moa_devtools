"""Menú interactivo para gestionar simuladores disponibles en MOA DevTools."""

import os
import subprocess
from typing import List

from utils.menu import mostrar_menu


procesos_simuladores: List[subprocess.Popen] = []


def _obtener_ruta_simuladores() -> str:
    """Obtiene la ruta absoluta al directorio de simuladores."""
    base_utils = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(base_utils, "simulators"))


def _listar_simuladores_disponibles() -> list[str]:
    """Lista las subcarpetas de simuladores disponibles."""
    ruta_simuladores = _obtener_ruta_simuladores()
    if not os.path.isdir(ruta_simuladores):
        return []

    subcarpetas = []
    for nombre in os.listdir(ruta_simuladores):
        ruta_completa = os.path.join(ruta_simuladores, nombre)
        if os.path.isdir(ruta_completa):
            subcarpetas.append(nombre)

    return sorted(subcarpetas)


def _construir_ruta_simulador(sim_name: str) -> str:
    """Construye la ruta absoluta al entrypoint de un simulador."""
    ruta_simuladores = _obtener_ruta_simuladores()
    return os.path.abspath(os.path.join(ruta_simuladores, sim_name, f"{sim_name}.py"))


def _iniciar_simulador(sim_name: str) -> None:
    """Inicia el simulador indicado y registra el proceso."""
    ruta_entrypoint = _construir_ruta_simulador(sim_name)

    if not os.path.exists(ruta_entrypoint):
        print(
            "No se encontró el entrypoint del simulador '",
            f"{sim_name}' en utils/simulators/{sim_name}/{sim_name}.py",
            sep="",
        )
        return

    try:
        proceso = subprocess.Popen(["python", ruta_entrypoint])
        procesos_simuladores.append(proceso)
        print(f"Simulador '{sim_name}' iniciado con PID {proceso.pid}.")
    except Exception as exc:
        print(f"No se pudo iniciar el simulador '{sim_name}': {exc}")


def _cerrar_instancias() -> None:
    """Cierra todas las instancias de simuladores iniciadas desde el menú."""
    if not procesos_simuladores:
        print("No se registran simuladores activos para cerrar.")
        return

    procesos_activos = 0
    for proceso in list(procesos_simuladores):
        if proceso.poll() is None:
            procesos_activos += 1
            try:
                proceso.terminate()
                proceso.wait(timeout=5)
                print(f"Simulador con PID {proceso.pid} finalizado correctamente.")
            except Exception as exc:
                print(f"No se pudo finalizar el simulador con PID {proceso.pid}: {exc}")
        procesos_simuladores.remove(proceso)

    if procesos_activos == 0:
        print("No se encontraron simuladores en ejecución.")


def _menu_parametros(sim_name: str) -> None:
    """Muestra el submenú de parámetros en construcción."""
    print("Pantalla en construcción. Presione 0 para volver.")
    while True:
        opcion = mostrar_menu(f"Parámetros del simulador {sim_name}", [], incluir_salida=True)
        if opcion == 0:
            break


def _menu_opciones_simulador(sim_name: str) -> None:
    """Despliega el submenú para operar sobre un simulador."""
    while True:
        opcion = mostrar_menu(
            f"Simulador: {sim_name}",
            [
                "Iniciar sin parámetros",
                "Iniciar con parámetros",
                "Cerrar todas las instancias",
            ],
        )

        if opcion == 0:
            break
        if opcion == 1:
            _iniciar_simulador(sim_name)
        elif opcion == 2:
            _menu_parametros(sim_name)
        elif opcion == 3:
            _cerrar_instancias()


def menu_simuladores() -> None:
    """Muestra el menú de simuladores disponibles."""
    while True:
        simuladores = _listar_simuladores_disponibles()
        if not simuladores:
            print("No se encontraron simuladores disponibles en utils/simulators/.")
            break

        opcion = mostrar_menu("Simuladores disponibles", simuladores)

        if opcion == 0:
            break

        indice = opcion - 1
        if 0 <= indice < len(simuladores):
            sim_name = simuladores[indice]
            _menu_opciones_simulador(sim_name)
        else:
            print("Opción inválida, seleccione un simulador válido.")
