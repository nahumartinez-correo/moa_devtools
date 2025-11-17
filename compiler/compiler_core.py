"""
Módulo central de compilación.
Define la lógica que permite compilar uno o varios archivos dentro de POST,
modificando el include del módulo correspondiente antes de ejecutar el
compilador, y usando la herramienta correcta según si se trata de un
archivo especial.
"""

import os
import subprocess
from utils.logger import log_info, log_error


COMANDO_BC = r'bc -npost -s -v -Ic:\moa\src\include'
CARPETA_MOAPROJ = r"C:\moaproj"

EXTENSIONES_ESPECIALES = {"fld", "dsc", "plb", "pat", "pic", "tag"}

# Backup para restaurar archivos especiales luego de la compilación
_BACKUP_ESPECIALES = {}


def compilar_lista_archivos(version, ruta_post, lista_relativa):
    """Compila una lista de archivos por ruta relativa dentro de POST."""
    log_info(f"Inicio de compilación múltiple. Total archivos: {len(lista_relativa)}")
    for rel in lista_relativa:
        ruta_abs = os.path.join(ruta_post, rel)
        compilar_archivo(version, ruta_post, ruta_abs)
    log_info("Finalizada compilación múltiple.")


def compilar_archivo(version, ruta_post, ruta_abs):
    """Compila un archivo individual, detectando si es especial o normal."""
    nombre = os.path.basename(ruta_abs)
    modulo = os.path.basename(os.path.dirname(ruta_abs))
    nombre_sin_ext = nombre.lower()

    log_info(f"Compilación solicitada para: {ruta_abs} (módulo: {modulo})")

    # Patch de include particular (postXXXX.h)
    _patch_include_particular(version, ruta_post, ruta_abs, modulo)

    # Archivos especiales (.fld, .pat, etc.)
    if nombre_sin_ext in EXTENSIONES_ESPECIALES:
        _patch_especial(version, ruta_abs)  # <<< NUEVO
        comando = _compilar_especial(version, nombre_sin_ext)
        log_info(f"Compilación identificada como especial: {comando}")
    else:
        comando = f'{COMANDO_BC} {ruta_abs}'
        log_info(f"Compilación estándar: {comando}")

    print(f"\nEjecutando: {comando}\n")
    _ejecutar_comando(comando)

    # Restaurar include particular al terminar
    _restaurar_include_particular(ruta_abs)

    # Restaurar archivo especial si corresponde
    _restaurar_especial(ruta_abs)  # <<< NUEVO


def _patch_include_particular(version, ruta_post, ruta_abs, modulo):
    """
    Reemplaza cualquier línea que comience con #include "post
    respetando el nombre real del header encontrado en el archivo.

    NO se basa en el nombre del módulo para construir el header.
    Simplemente inserta la ruta absoluta dentro del include existente.
    """

    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.readlines()
    except Exception as e:
        log_error(f"No fue posible leer el archivo {ruta_abs}: {e}")
        return

    nuevas = []
    modificado = False

    for linea in lineas:
        l = linea.strip()

        # Detecta líneas del tipo:  #include "postXXXX.h"
        if l.startswith('#include "post') and l.endswith('.h"'):

            log_info(f"Include particular detectado: {l}")

            # Extrae sólo el nombre que ya existe, respetando mayúsculas/minúsculas
            inicio = '#include "'
            idx = linea.find(inicio) + len(inicio)
            header_real = linea[idx:].strip().rstrip('"')

            # Construye ruta absoluta correcta
            ruta_dir = os.path.dirname(ruta_abs)
            ruta_completa = os.path.join(ruta_dir, header_real)
            ruta_completa = ruta_completa.replace("\\", "\\\\")

            nueva = f'#include "{ruta_completa}"\n'
            nuevas.append(nueva)

            log_info(f"Include reemplazado por: {nueva.strip()}")
            modificado = True
        else:
            nuevas.append(linea)

    if modificado:
        try:
            with open(ruta_abs, "w", encoding="utf-8") as f:
                f.writelines(nuevas)
            log_info(f"Archivo actualizado correctamente: {ruta_abs}")
        except Exception as e:
            log_error(f"Error escribiendo archivo {ruta_abs}: {e}")
    else:
        log_info("No se detectó include particular para reemplazar.")


def _patch_especial(version, ruta_abs):
    """
    Aplica reemplazos de includes generales dentro de un archivo especial
    (.fld, .dsc, .plb, etc.) y guarda un backup para restaurar luego.
    """

    if ruta_abs in _BACKUP_ESPECIALES:
        return  # ya estaba parcheado

    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="ignore") as f:
            original = f.read()
    except Exception:
        return

    _BACKUP_ESPECIALES[ruta_abs] = original  # backup

    # Obtener reemplazos generales
    from compiler.includes_manager import obtener_reemplazos_generales
    reemplazos = obtener_reemplazos_generales(version)

    nuevo = original
    for viejo, nuevo_val in reemplazos.items():
        nuevo = nuevo.replace(viejo, nuevo_val)

    if nuevo != original:
        try:
            with open(ruta_abs, "w", encoding="utf-8") as f:
                f.write(nuevo)
            log_info(f"Archivo especial actualizado: {ruta_abs}")
        except Exception:
            pass


def _restaurar_especial(ruta_abs):
    """Restaura el archivo especial modificado durante la compilación."""
    if ruta_abs not in _BACKUP_ESPECIALES:
        return

    try:
        with open(ruta_abs, "w", encoding="utf-8") as f:
            f.write(_BACKUP_ESPECIALES[ruta_abs])
        log_info(f"Archivo especial restaurado: {ruta_abs}")
    except Exception:
        pass

    del _BACKUP_ESPECIALES[ruta_abs]


def _compilar_especial(version, nombre):
    """Construye el comando para compilar un archivo especial."""
    return f"imp{nombre} -npost C:\\moaproj\\{version}\\src\\POST\\{nombre}"


def _ejecutar_comando(cmd):
    """Ejecuta el comando del compilador mostrando salida en tiempo real."""
    log_info(f"Ejecutando comando: {cmd}")
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        for linea in process.stdout:
            print(linea.strip())

        process.wait()

        if process.returncode == 0:
            print("\n✔ Compilación finalizada correctamente.\n")
            log_info("Compilación finalizada correctamente.")
        else:
            print("\n✖ Error de compilación.\n")
            log_error(f"Error de compilación. Código: {process.returncode}")

    except Exception as e:
        log_error(f"Error ejecutando compilación: {e}")
        print(f"\nError inesperado: {e}")


def _restaurar_include_particular(ruta_abs):
    """
    Revierte la línea de include particular, buscando líneas que empiecen con
    #include "C: y reconstruyendo el include original.
    """

    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.readlines()
    except Exception:
        return

    nuevas = []
    cambiado = False

    for linea in lineas:
        l = linea.strip()

        # Detectar include parcheado (ruta absoluta)
        if l.lower().startswith('#include "c:'):
            parte = l.split("\\")[-1]   # postPRES.h"
            nuevo_include = f'#include "{parte}'
            nuevas.append(nuevo_include + "\n")
            cambiado = True
            continue

        nuevas.append(linea)

    if not cambiado:
        return

    try:
        with open(ruta_abs, "w", encoding="utf-8") as f:
            f.writelines(nuevas)
        log_info(f"Include restaurado en {ruta_abs}")
    except Exception as e:
        log_error(f"Error restaurando include en {ruta_abs}: {e}")