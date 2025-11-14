import os
import time
from utils.logger import log_info, log_error

# --- CONFIGURACIÓN BASE ---
CARPETA_MOAPROJ = r"C:\moaproj"

# --- Lista de reemplazos generales ---
def obtener_reemplazos_generales(version):
    base = rf"C:\\moaproj\\{version}\\src\\INCLUDE"
    ofb = r"C:\\MOA\\src\\include\\ofb"

    return {
        '#include "drv.h"':          fr'#include "{base}\\drv.h"',
        '#include "ofbdefs.h"':      fr'#include "{base}\\ofbdefs.h"',
        '#include "keys.h"':         fr'#include "{base}\\keys.h"',
        '#include "presupuesto.h"':  fr'#include "{base}\\presupuesto.h"',
        '#include "impresio.h"':     fr'#include "{base}\\impresio.h"',
        '#include "tesoro.h"':       fr'#include "{base}\\tesoro.h"',
        '#include "csr.h"':          fr'#include "{base}\\csr.h"',
        '#include <csr.h>':          fr'#include "{base}\\csr.h"',
        '#include "base.h"':         fr'#include "{base}\\base.h"',
        '#include "admin_dt.h"':     fr'#include "{base}\\admin_dt.h"',
        '#include "pickdrv.h"':      fr'#include "{base}\\pickdrv.h"',
        '#include "giros.h"':        fr'#include "{base}\\giros.h"',
        '#include "hcommstd.h"':     fr'#include "{base}\\hcommstd.h"',
        '#include "Sap.h"':          fr'#include "{base}\\Sap.h"',
        '#include "sap.h"':          fr'#include "{base}\\Sap.h"',
        '#include "sf1.h"':          fr'#include "{base}\\sf1.h"',
        '#include "sucuvirt.h"':     fr'#include "{base}\\sucuvirt.h"',
        '#include "commdef.h"':      fr'#include "{base}\\commdef.h"',
        '#include "descuento.h"':    fr'#include "{base}\\descuento.h"',
        '#include "bonif.h"':        fr'#include "{base}\\bonif.h"',
        '#include "reporte.h"':      fr'#include "{base}\\reporte.h"',
        '#include "postscr.h"':      fr'#include "C:\\moaproj\\{version}\\src\\POST\\scr\\postscr.h"',
        '#include "cdserdef.h"':     fr'#include "{ofb}\\cdserdef.h"',
        '#include "desktop.h"':      fr'#include "{ofb}\\desktop.h"',
        '#include "field.h"':        fr'#include "{ofb}\\field.h"',
        '#include "gsp.h"':          fr'#include "{base}\\gsp.h"',
        '#include "Hcommstd.h"':     fr'#include "{base}\\Hcommstd.h"',
    }


def _reemplazar_contenido(path, reemplazos):
    """Reemplaza en el archivo todos los pares del diccionario."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
    except Exception:
        return False

    nuevo = data
    for viejo, nuevo_val in reemplazos.items():
        nuevo = nuevo.replace(viejo, nuevo_val)
    if nuevo != data:
        with open(path, "w", encoding="utf-8") as f:
            f.write(nuevo)
        return True
    return False


def _obtener_version_desde_ruta(archivo):
    """Detecta automáticamente la versión (ej: V47.09) desde la ruta del archivo."""
    partes = archivo.split(os.sep)
    for p in partes:
        if p.upper().startswith("V") and "." in p:
            return p
    return "V00.00"  # fallback


def actualizar_includes(archivo):
    """Actualiza los includes generales en todos los archivos del proyecto para la versión detectada."""
    version = _obtener_version_desde_ruta(archivo)
    carpeta_src = os.path.join(CARPETA_MOAPROJ, version, "src")

    print(f"🛠  Actualizando includes generales para versión {version}...")
    log_info(f"Iniciando actualización de includes generales ({version})...")

    reemplazos = obtener_reemplazos_generales(version)
    modificados = []

    # Archivos especiales reconocidos (sin extensión)
    especiales = {"fld", "dsc", "plb"}

    for root, _, files in os.walk(carpeta_src):
        for file in files:
            nombre, ext = os.path.splitext(file)
            ext = ext.lower().lstrip(".")

            # ✅ Aceptamos también archivos sin extensión o especiales
            if ext in ("c", "cpp", "h") or (ext == "" and nombre.lower() in especiales):
                path = os.path.join(root, file)
                if _reemplazar_contenido(path, reemplazos):
                    modificados.append(path)

    print(f"✅ Includes generales modificados en {len(modificados)} archivos.")
    log_info(f"Includes generales modificados en {len(modificados)} archivos.")
    time.sleep(1)
    return modificados



def actualizar_include_modulo(archivo):
    """Actualiza el include particular del módulo del archivo especificado."""
    version = _obtener_version_desde_ruta(archivo)
    dir_modulo = os.path.basename(os.path.dirname(archivo))
    nombre_header = f'post{dir_modulo}.h'

    print(f"🧩 Actualizando include particular del módulo {dir_modulo}...")
    include_original = f'#include "{nombre_header}"'
    include_completo = f'#include "C:\\\\moaproj\\\\{version}\\\\src\\\\POST\\\\{dir_modulo}\\\\{nombre_header}"'
    reemplazos = {include_original: include_completo}

    _reemplazar_contenido(archivo, reemplazos)
    log_info(f"Include particular actualizado para módulo {dir_modulo}.")
    return include_original, include_completo


def restaurar_includes(modificados):
    """Restaura los includes generales modificados."""
    if not modificados:
        print("⚙️  No hay includes para restaurar.")
        return

    print("🔄 Restaurando includes generales...")
    # Detectamos la versión de alguno de los archivos modificados
    version = _obtener_version_desde_ruta(modificados[0])
    reemplazos = obtener_reemplazos_generales(version)
    inverso = {v: k for k, v in reemplazos.items()}

    for path in modificados:
        _reemplazar_contenido(path, inverso)

    print("✅ Includes generales restaurados.")
    log_info("Includes generales restaurados correctamente.")
