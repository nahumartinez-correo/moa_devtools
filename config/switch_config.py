import os
import subprocess
import time
from utils.logger import log_info, log_error

# --- CONFIGURACIÓN ---
ARCHIVO_SWITCH = r"C:\Program Files\SwitchDemand\SwitchDemand.ini"

CONFIGURACIONES = {
    1: {
        "descripcion": "Emulador para las pruebas de MercadoPago - Smart Point",
        "ip": "127.0.0.1",
        "port": "9999"
    },
    2: {
        "descripcion": "OpenShift de MercadoPago - Smart Point",
        "ip": "10.1.21.27",
        "port": "32005"
    },
    3: {
        "descripcion": "IP de la PC de Ramiro para pruebas de MercadoPago - Smart Point",
        "ip": "10.254.128.130",
        "port": "5005"
    },
    4: {
        "descripcion": "DNS de la PC de Ramiro para pruebas de MercadoPago - Smart Point",
        "ip": "ws-interfaz-mosaic-mp-tcp-ws-interfaz-mosaic-mp-dev.apps.ocpbarr.correo.local",
        "port": "32005"
    },
}


# --- CONTROL DE SERVICIOS ---
def _ejecutar(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def servicio_activo(nombre):
    return "RUNNING" in _ejecutar(f'sc query "{nombre}"')


def detener_servicio(nombre):
    """Detiene un servicio con feedback visual."""
    print(f"⏳ Deteniendo {nombre}...")
    _ejecutar(f'sc stop "{nombre}"')
    for _ in range(6):
        time.sleep(1)
        if not servicio_activo(nombre):
            print(f"✅ {nombre} detenido correctamente.")
            return True
    print(f"⚠ No se pudo detener el servicio {nombre}.")
    return False


def iniciar_servicio(nombre):
    """Inicia un servicio con feedback visual."""
    print(f"⏳ Iniciando {nombre}...")
    _ejecutar(f'sc start "{nombre}"')
    for _ in range(6):
        time.sleep(1)
        if servicio_activo(nombre):
            print(f"✅ {nombre} iniciado correctamente.")
            return True
    print(f"⚠ El servicio {nombre} no se inició correctamente.")
    return False


# --- MODIFICACIÓN DE ARCHIVO ---
def actualizar_configuracion(opcion):
    """Actualiza el bloque [port14] con los valores de la opción indicada."""
    if opcion not in CONFIGURACIONES:
        raise ValueError("Opción inválida")

    config = CONFIGURACIONES[opcion]

    if not os.path.exists(ARCHIVO_SWITCH):
        raise FileNotFoundError(f"No se encontró el archivo: {ARCHIVO_SWITCH}")

    with open(ARCHIVO_SWITCH, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    nuevas_lineas = []
    dentro_port14 = False

    for linea in lineas:
        if linea.strip().startswith("[port14]"):
            dentro_port14 = True
            nuevas_lineas.append(linea)
            continue

        if dentro_port14 and linea.strip().startswith("["):
            dentro_port14 = False

        if dentro_port14:
            if linea.strip().startswith("descripcion="):
                nuevas_lineas.append(f"descripcion={config['descripcion']}\n")
            elif linea.strip().startswith("ip="):
                nuevas_lineas.append(f"ip={config['ip']}\n")
            elif linea.strip().startswith("port="):
                nuevas_lineas.append(f"port={config['port']}\n")
            else:
                nuevas_lineas.append(linea)
        else:
            nuevas_lineas.append(linea)

    with open(ARCHIVO_SWITCH, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

    log_info(f"Archivo {ARCHIVO_SWITCH} actualizado (modo {config['descripcion']})")
