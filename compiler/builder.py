"""
Módulo principal del compilador de MOA DevTools.
Incluye:
 - Validación de permisos de administrador.
 - Verificación de servicios detenidos antes de compilar.
 - Limpieza visual de la consola entre pasos.
"""

import os
from utils.menu import mostrar_menu
from utils.logger import log_info, log_error
from utils.permissions import es_administrador
from utils import service_manager
from compiler import svn_manager, includes_manager, compiler_runner

CARPETA_MOAPROJ = r"C:\moaproj"


def limpiar_consola():
    """Limpia la pantalla y muestra el encabezado."""
    os.system("cls")
    print("=" * 70)
    print("        MOA DevTools - COMPILADOR DE VERSIONES POST")
    print("=" * 70, "\n")


def verificar_servicios_detendidos():
    """
    Intenta detener todos los servicios requeridos.
    Devuelve True si todos se detuvieron correctamente.
    """
    print("\n🧱 Deteniendo servicios requeridos...\n")
    log_info("Intentando detener servicios para compilación...")

    resultado = service_manager.detener_todos()
    if not resultado:
        print("❌ No se pudieron detener todos los servicios. No se puede compilar.")
        log_error("No se pudieron detener los servicios.")
        return False

    print("✅ Todos los servicios detenidos correctamente.\n")
    return True


def menu_compilador():
    """Muestra el menú principal del compilador."""
    while True:
        limpiar_consola()

        if not es_administrador():
            print("⚠️  No tiene permisos de administrador.")
            print("   Ejecute el script en modo administrador para poder compilar.\n")
            input("Presione ENTER para volver al menú principal...")
            return

        print("Verificación de permisos: OK ✅\n")

        versiones = svn_manager.obtener_versiones(CARPETA_MOAPROJ)
        if not versiones:
            print("⚠️  No se encontraron carpetas de versión (formato Vxx.yy).")
            input("Presione ENTER para volver al menú principal...")
            return

        opcion = mostrar_menu("Seleccione la versión del proyecto", versiones)
        if opcion == 0:
            return

        version_sel = versiones[opcion - 1]
        ruta_version = os.path.join(CARPETA_MOAPROJ, version_sel)

        limpiar_consola()
        print(f"Buscando archivos modificados en {version_sel}...\n")
        modificados = svn_manager.listar_cambios_svn(ruta_version)

        # Filtrar solo los que no sean .h
        modificados_filtrados = [f for f in modificados if not f.lower().endswith(".h")]

        if not modificados_filtrados:
            print("✅ No hay archivos modificados para compilar (excluyendo headers).")
            input("Presione ENTER para volver al menú anterior...")
            return

        opcion_archivo = mostrar_menu("Archivos modificados detectados", modificados_filtrados)
        if opcion_archivo == 0:
            continue

        archivo_sel = modificados_filtrados[opcion_archivo - 1]
        ruta_completa = os.path.join(ruta_version, archivo_sel)

        limpiar_consola()
        if not verificar_servicios_detendidos():
            input("Presione ENTER para volver al menú anterior...")
            continue

        limpiar_consola()
        print(f"Compilando archivo:\n{ruta_completa}\n")
        compiler_runner.compilar_archivo(ruta_completa)

        print("\n✅ Proceso finalizado correctamente.")
        input("Presione ENTER para volver al menú anterior...")
