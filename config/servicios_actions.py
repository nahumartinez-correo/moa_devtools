"""
Acciones simples de servicios para el menú de configuración.
"""

from config.constants import SERVICIOS
from utils import service_manager
from utils.logger import log_info, log_error


def detener_servicios():
    print("Deteniendo servicios...")
    if service_manager.detener_servicios(SERVICIOS):
        log_info("Servicios detenidos correctamente.")
        return True
    log_error("No se pudieron detener todos los servicios.")
    return False


def iniciar_servicios():
    print("Iniciando servicios...")
    service_manager.iniciar_servicios(SERVICIOS)
    log_info("Inicio de servicios solicitado.")
    return True
