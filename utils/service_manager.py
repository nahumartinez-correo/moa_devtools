import subprocess
import time
from utils.logger import log_info, log_error

SERVICIOS = [
    "CDS_post01gene",
    "CDS_post01main",
    "SwitchDemand",
    "RTBatch"
]


def _ejecutar(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def _servicio_activo(nombre):
    return "RUNNING" in _ejecutar(f'sc query "{nombre}"')


def detener_todos():
    print("\n🧱 Deteniendo servicios...")
    todos_ok = True
    for s in SERVICIOS:
        print(f"   ⏳ Deteniendo {s}...")
        if _servicio_activo(s):
            _ejecutar(f'sc stop "{s}"')
            for _ in range(3):
                time.sleep(1)
                if not _servicio_activo(s):
                    print(f"   ✅ {s} detenido.")
                    log_info(f"{s} detenido correctamente.")
                    break
            else:
                print(f"   ❌ No se pudo detener {s}.")
                log_error(f"No se pudo detener {s}.")
                todos_ok = False
        else:
            print(f"   ⚙️  {s} ya estaba detenido.")
            log_info(f"{s} ya estaba detenido.")
    return todos_ok


def iniciar_todos():
    print("\n🚀 Iniciando servicios...")
    for s in SERVICIOS:
        print(f"   ⏳ Iniciando {s}...")
        _ejecutar(f'sc start "{s}"')
        for _ in range(3):
            time.sleep(1)
            if _servicio_activo(s):
                print(f"   ✅ {s} iniciado correctamente.")
                log_info(f"{s} iniciado correctamente.")
                break
        else:
            print(f"   ❌ El servicio {s} no se inició correctamente.")
            log_error(f"El servicio {s} no se inició correctamente.")
