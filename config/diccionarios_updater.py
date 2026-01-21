"""
Rutina de actualización de diccionarios por integración.
"""

import glob
import os
import shutil
import subprocess

from utils import service_manager
from utils.logger import log_info, log_error
from compiler.includes_manager import obtener_reemplazos_generales


BASE_MOAPROJ = r"C:\moaproj"
RUTA_POST = os.path.join(BASE_MOAPROJ, "post")
RUTA_GIT = os.path.join(BASE_MOAPROJ, "Mosaic-gitlab")
RUTA_GIT_SRC = os.path.join(RUTA_GIT, "src")
RUTA_CDSGENE_POST = os.path.join(RUTA_POST, "cdsgene")
RUTA_CDSMAIN_POST = os.path.join(RUTA_POST, "cdsmain")
RUTA_CDSGENE_GIT = os.path.join(RUTA_GIT, "cdsgene")
RUTA_CDSMAIN_GIT = os.path.join(RUTA_GIT, "cdsmain")
RUTA_PASSWORD = os.path.join(BASE_MOAPROJ, "password")
RUTA_INIT_SUC = os.path.join(BASE_MOAPROJ, "scripts", "InitSuc")
RUTA_OPER_TEST = os.path.join(BASE_MOAPROJ, "scripts", "Oper_Test")

SERVICIOS = ["CDS_post01gene", "CDS_post01main"]
ENV = "post"
SUCURSAL = "B0016"


def actualizar_diccionarios_por_integracion():
    log_info("Inicio de actualización de diccionarios por integración.")
    servicios_detenidos = False
    headers_backup = None
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
        headers_backup = _aplicar_reemplazos_includes()

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
        )

        print("Restaurando headers...")
        _restaurar_headers(headers_backup)
        headers_backup = None

        print("Iniciando servicios...")
        service_manager.iniciar_servicios(SERVICIOS)

        print("Ejecutando InitSuc...")
        _ejecutar_comando(
            ["cmd", "/c", "InitSuc.bat", ENV, SUCURSAL],
            "InitSuc",
            cwd=RUTA_INIT_SUC,
        )

        print("Ejecutando oper_test...")
        _ejecutar_comando(
            ["perl", "oper_test.pl", ENV, SUCURSAL],
            "oper_test",
            cwd=RUTA_OPER_TEST,
        )

        exito = True
        log_info("Actualización de diccionarios finalizada correctamente.")
        return True
    except Exception as exc:
        log_error(f"Error en actualización de diccionarios: {exc}")
        print("Ocurrió un error durante la actualización. Revisar logs.")
        return False
    finally:
        if headers_backup:
            print("Restaurando headers tras error...")
            _restaurar_headers(headers_backup)
        if servicios_detenidos and not exito:
            print("Intentando recuperar servicios...")
            log_info("Intentando iniciar servicios tras error.")
            service_manager.iniciar_servicios(SERVICIOS)


def _validar_rutas():
    rutas = [
        RUTA_POST,
        RUTA_GIT,
        RUTA_GIT_SRC,
        RUTA_CDSGENE_POST,
        RUTA_CDSMAIN_POST,
        RUTA_CDSGENE_GIT,
        RUTA_CDSMAIN_GIT,
        RUTA_PASSWORD,
        RUTA_INIT_SUC,
        RUTA_OPER_TEST,
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


def _ejecutar_comando(cmd, descripcion, cwd=None):
    log_info(f"Ejecutando comando: {descripcion}")
    resultado = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if resultado.returncode != 0:
        log_error(
            f"Comando falló ({descripcion}). STDOUT: {resultado.stdout} "
            f"STDERR: {resultado.stderr}"
        )
        raise RuntimeError(f"Comando falló: {descripcion}")
    if resultado.stdout:
        log_info(f"{descripcion} STDOUT: {resultado.stdout.strip()}")
    if resultado.stderr:
        log_error(f"{descripcion} STDERR: {resultado.stderr.strip()}")


def _aplicar_reemplazos_includes():
    reemplazos = obtener_reemplazos_generales("Mosaic-gitlab")
    if not reemplazos:
        return {}

    headers_backup = {}
    for root, _, files in os.walk(RUTA_GIT_SRC):
        for nombre in files:
            if not nombre.lower().endswith(".h"):
                continue
            ruta = os.path.join(root, nombre)
            try:
                with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                    contenido = f.read()
            except Exception as exc:
                log_error(f"No fue posible leer {ruta}: {exc}")
                raise

            nuevo = contenido
            cambios = 0
            for viejo, nuevo_val in reemplazos.items():
                if viejo in nuevo:
                    cambios += nuevo.count(viejo)
                nuevo = nuevo.replace(viejo, nuevo_val)

            if cambios == 0 or nuevo == contenido:
                continue

            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(nuevo)
                headers_backup[ruta] = contenido
                log_info(f"Header actualizado: {ruta}")
            except Exception as exc:
                log_error(f"No fue posible escribir {ruta}: {exc}")
                raise

    return headers_backup


def _restaurar_headers(headers_backup):
    if not headers_backup:
        return

    for ruta, contenido in headers_backup.items():
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            log_info(f"Header restaurado: {ruta}")
        except Exception as exc:
            log_error(f"No se pudo restaurar {ruta}: {exc}")
