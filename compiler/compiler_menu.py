"""
Módulo que implementa el menú del compilador. Gestiona el flujo completo:
verificación de permisos, selección de versión, obtención de cambios en SVN,
compilación individual o masiva, y reversión de headers al finalizar.
"""

import os
import subprocess
from utils.menu import mostrar_menu
from utils.permissions import es_administrador
from utils.logger import log_info, log_error
from utils.service_manager import detener_todos, iniciar_todos
from compiler.session_state import SessionState
from compiler.svn_changes import obtener_archivos_modificados
from compiler.include_patcher import aplicar_patches_generales
from compiler.compiler_core import compilar_archivo, compilar_lista_archivos
from compiler.restore_manager import revertir_headers


CARPETA_MOAPROJ = r"C:\moaproj"


def menu_compilador():
    """
    Flujo principal del menú de compilación. Controla la preparación previa,
    la interacción con el usuario y la restauración final.
    """
    if not es_administrador():
        print("\n⚠ No se poseen privilegios de administrador.")
        print("   No es posible acceder al menú de compilación.\n")
        input("Presione ENTER para continuar...")
        return

    detener_todos()

    estado = SessionState()

    while True:
        _limpiar_pantalla()
        print("=== COMPILADOR — MOA DevTools ===\n")

        version = _seleccionar_version()
        if not version:
            _finalizar_menu(estado)
            return

        estado.version = version

        ruta_post = os.path.join(CARPETA_MOAPROJ, version, "src")

        _limpiar_pantalla()
        print("=== COMPILADOR — Preparando entorno ===\n")

        estado.modificados_h = aplicar_patches_generales(version)

        archivos = obtener_archivos_modificados(ruta_post)
        if not archivos:
            print("No se encontraron archivos modificados en SVN.\n")
            input("Presione ENTER para volver...")
            continue

        _sub_menu_compilacion(estado, ruta_post, archivos)


def _seleccionar_version():
    """
    Lista las carpetas de versión (Vxx.xx) dentro de moaproj y permite seleccionar una.
    """
    try:
        versiones = sorted(
            [d for d in os.listdir(CARPETA_MOAPROJ) if d.upper().startswith("V")],
            reverse=True
        )
    except Exception:
        return None

    opcion = mostrar_menu("Seleccione la versión a compilar", versiones)
    if opcion == 0:
        return None

    return versiones[opcion - 1]


def _sub_menu_compilacion(estado, ruta_post, archivos_relativos):
    """
    Presenta el listado de archivos modificados permitiendo compilar uno o varios.
    """
    while True:
        _limpiar_pantalla()
        print("=== ARCHIVOS MODIFICADOS EN SVN ===\n")
        print("Ruta base:", ruta_post, "\n")

        for i, a in enumerate(archivos_relativos, 1):
            print(f"{i}) {a}")

        print("\n0) Volver")
        print("T) Compilar todos los archivos\n")

        sel = input("Seleccione un archivo o 'T': ").strip().lower()

        if sel == "0":
            return

        if sel == "t":
            compilar_lista_archivos(estado.version, ruta_post, archivos_relativos)
            input("Presione ENTER para continuar...")
            continue

        try:
            idx = int(sel)
            if 1 <= idx <= len(archivos_relativos):
                rel = archivos_relativos[idx - 1]
                ruta_abs = os.path.join(ruta_post, rel)
                compilar_archivo(estado.version, ruta_post, ruta_abs)
                input("Presione ENTER para continuar...")
        except ValueError:
            continue


def _finalizar_menu(estado):
    """
    Restaura los headers modificados y reinicia los servicios detenidos.
    """
    _limpiar_pantalla()
    print("=== FINALIZANDO COMPILADOR ===\n")

    if estado.modificados_h:
        print("Revirtiendo modificaciones en headers...\n")
        revertir_headers(estado.modificados_h)
    else:
        print("No se detectaron headers modificados.\n")

    iniciar_todos()
    input("\nPresione ENTER para continuar...")


def _limpiar_pantalla():
    """Limpia la consola."""
    os.system("cls")
