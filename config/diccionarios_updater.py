"""
Rutina de actualización de diccionarios por integración.
"""

import glob
import os
import shutil
import subprocess

from config.constants import (
    RUTA_POST,
    RUTA_GIT,
    RUTA_CDSGENE_POST,
    RUTA_CDSMAIN_POST,
    RUTA_CDSGENE_GIT,
    RUTA_CDSMAIN_GIT,
    RUTA_PASSWORD,
    SERVICIOS,
)
from config.includes_updater import aplicar_includes, revertir_includes
from utils import service_manager
from utils.logger import log_info, log_error


def actualizar_diccionarios_por_integracion():
    log_info("Inicio de actualización de diccionarios por integración.")
    servicios_detenidos = False
    exito = False

    try:
        _validar_rutas()

        print("Deteniendo servicios...")
        if not service_manager.detener_servicios(SERVICIOS):
            log_error("No fue posible detener todos los servicios requeridos.")
            print("Error al detener servicios. Operación abortada.")
            return False
        servicios_detenidos = True

        print("Borrando archivos DDnotes.* y DDobj.* en post...")
        _eliminar_patrones(RUTA_POST, ["DDnotes.*", "DDobj.*"])

        print("Vaciando carpetas cdsgene y cdsmain...")
        _vaciar_directorio(RUTA_CDSGENE_POST)
        _vaciar_directorio(RUTA_CDSMAIN_POST)

        print("Copiando archivos DDnotes.* y DDobj.* desde Mosaic-gitlab...")
        _copiar_patrones(RUTA_GIT, RUTA_POST, ["DDnotes.*", "DDobj.*"])

        print("Copiando contenido de cdsgene...")
        _copiar_contenido(RUTA_CDSGENE_GIT, RUTA_CDSGENE_POST)

        print("Copiando contenido de cdsmain...")
        _copiar_contenido(RUTA_CDSMAIN_GIT, RUTA_CDSMAIN_POST)

        print("Aplicando reemplazos de includes en headers...")
        if not aplicar_includes():
            log_error("No fue posible aplicar los includes.")
            return False

        print("Compilando password...")
        _ejecutar_comando(
            [
                "bc",
                "-npost",
                "-s",
                "-v",
                r"-Ic:\moa\src\include",
                RUTA_PASSWORD,
            ],
            "Compilación de password",
            ignore_stderr_substrings=[
                "Source file 'C:\\moaproj\\password' not in directory path for project: post"
            ],
            ignore_stderr_if_match=True,
        )

        print("Restaurando headers...")
        if not revertir_includes():
            log_error("No fue posible revertir los includes.")
            return False

        print("Iniciando servicios...")
        service_manager.iniciar_servicios(SERVICIOS)

        exito = True
        log_info("Actualización de diccionarios finalizada correctamente.")
        return True
    except Exception as exc:
        log_error(f"Error en actualización de diccionarios: {exc}")
        print("Ocurrió un error durante la actualización. Revisar logs.")
        return False
    finally:
        if not exito:
            print("Restaurando headers tras error...")
            revertir_includes()
        if servicios_detenidos and not exito:
            print("Intentando recuperar servicios...")
            log_info("Intentando iniciar servicios tras error.")
            service_manager.iniciar_servicios(SERVICIOS)


def _validar_rutas():
    rutas = [
        RUTA_POST,
        RUTA_GIT,
        RUTA_CDSGENE_POST,
        RUTA_CDSMAIN_POST,
        RUTA_CDSGENE_GIT,
        RUTA_CDSMAIN_GIT,
        RUTA_PASSWORD,
    ]
    for ruta in rutas:
        if not os.path.exists(ruta):
            log_error(f"Ruta requerida no encontrada: {ruta}")
            raise FileNotFoundError(f"Ruta requerida no encontrada: {ruta}")


def _eliminar_patrones(directorio, patrones):
    for patron in patrones:
        for ruta in glob.glob(os.path.join(directorio, patron)):
            if os.path.isfile(ruta):
                try:
                    os.remove(ruta)
                    log_info(f"Archivo eliminado: {ruta}")
                except Exception as exc:
                    log_error(f"No se pudo eliminar {ruta}: {exc}")
                    raise


def _vaciar_directorio(directorio):
    if not os.path.isdir(directorio):
        log_error(f"Directorio no encontrado: {directorio}")
        raise FileNotFoundError(f"Directorio no encontrado: {directorio}")

    for nombre in os.listdir(directorio):
        ruta = os.path.join(directorio, nombre)
        try:
            if os.path.isdir(ruta):
                shutil.rmtree(ruta)
            else:
                os.remove(ruta)
            log_info(f"Elemento eliminado: {ruta}")
        except Exception as exc:
            log_error(f"No se pudo eliminar {ruta}: {exc}")
            raise


def _copiar_patrones(origen, destino, patrones):
    for patron in patrones:
        rutas = glob.glob(os.path.join(origen, patron))
        if not rutas:
            log_error(f"No se encontraron archivos para el patrón {patron} en {origen}")
            raise FileNotFoundError(f"No se encontraron archivos {patron} en {origen}")
        for ruta in rutas:
            destino_ruta = os.path.join(destino, os.path.basename(ruta))
            try:
                shutil.copy2(ruta, destino_ruta)
                log_info(f"Archivo copiado: {ruta} -> {destino_ruta}")
            except Exception as exc:
                log_error(f"No se pudo copiar {ruta}: {exc}")
                raise


def _copiar_contenido(origen, destino):
    if not os.path.isdir(origen):
        log_error(f"Directorio de origen no encontrado: {origen}")
        raise FileNotFoundError(f"Directorio de origen no encontrado: {origen}")
    if not os.path.isdir(destino):
        log_error(f"Directorio de destino no encontrado: {destino}")
        raise FileNotFoundError(f"Directorio de destino no encontrado: {destino}")

    for root, dirs, files in os.walk(origen):
        rel = os.path.relpath(root, origen)
        destino_root = os.path.join(destino, rel) if rel != "." else destino
        os.makedirs(destino_root, exist_ok=True)
        for d in dirs:
            os.makedirs(os.path.join(destino_root, d), exist_ok=True)
        for archivo in files:
            origen_ruta = os.path.join(root, archivo)
            destino_ruta = os.path.join(destino_root, archivo)
            try:
                shutil.copy2(origen_ruta, destino_ruta)
                log_info(f"Archivo copiado: {origen_ruta} -> {destino_ruta}")
            except Exception as exc:
                log_error(f"No se pudo copiar {origen_ruta}: {exc}")
                raise


def _ejecutar_comando(
    cmd,
    descripcion,
    cwd=None,
    ignore_stderr_substrings=None,
    ignore_stderr_if_match=False,
):
    log_info(f"Ejecutando comando: {descripcion}")
    resultado = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    stderr = resultado.stderr or ""
    ignore_stderr_substrings = ignore_stderr_substrings or []
    hay_match = any(fragmento in stderr for fragmento in ignore_stderr_substrings)
    stderr_lineas = stderr.splitlines()
    stderr_filtrado = [
        linea
        for linea in stderr_lineas
        if not any(fragmento in linea for fragmento in ignore_stderr_substrings)
    ]
    stderr_filtrado_texto = "\n".join(stderr_filtrado).strip()

    if resultado.returncode != 0:
        if ignore_stderr_if_match and hay_match:
            log_info(f"Comando con warning ignorado ({descripcion}).")
        elif ignore_stderr_substrings and not stderr_filtrado_texto:
            log_info(f"Comando con warning ignorado ({descripcion}).")
        else:
            log_error(
                f"Comando falló ({descripcion}). STDOUT: {resultado.stdout} "
                f"STDERR: {resultado.stderr}"
            )
            raise RuntimeError(f"Comando falló: {descripcion}")
    if resultado.stdout:
        log_info(f"{descripcion} STDOUT: {resultado.stdout.strip()}")
    if stderr_filtrado_texto and not (ignore_stderr_if_match and hay_match):
        log_error(f"{descripcion} STDERR: {stderr_filtrado_texto}")
