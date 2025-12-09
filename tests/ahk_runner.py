import os
import subprocess
import time
from utils.menu import mostrar_menu
from utils.permissions import es_administrador
from utils.logger import log_info, log_error
from utils.common import limpiar_consola
from config import session_state
from tests import simulators_manager


ENCABEZADO_PRUEBAS = "MOA DevTools - PRUEBAS AUTOMÁTICAS"


def obtener_lista_tests():
    """Obtiene los archivos .ahk válidos (que comiencen con 'test_')."""
    carpeta_tests = os.path.join(os.path.dirname(__file__), "codes")
    tests = []

    for nombre in os.listdir(carpeta_tests):
        if nombre.lower().startswith("test_") and nombre.lower().endswith(".ahk"):
            ruta = os.path.join(carpeta_tests, nombre)
            nombre_legible = (
                "Test - "
                + nombre[5:-4].replace("_", " ").capitalize()
            )
            tests.append((nombre_legible, ruta))
    return sorted(tests, key=lambda x: x[0].lower())


def preparar_entorno_tablas(nombre_prueba):
    """Ejecuta el script de manejo de tablas para preparar los datos previos a la prueba."""
    ruta_script = os.path.join(os.path.dirname(__file__), "mosaic_table_manager.py")
    ruta_setups = os.path.join(os.path.dirname(__file__), "set_up_tests", nombre_prueba)

    if not os.path.isdir(ruta_setups):
        return False  # No hay setup para esta prueba

    print(f"⚙️  Preparando entorno de tablas para la prueba '{nombre_prueba}'...\n")

    mostrar_datos = session_state.get_mostrar_datos_tablas()
    cmd = ["python", ruta_script, nombre_prueba]
    if mostrar_datos:
        cmd.append("--mostrar")

    try:
        subprocess.run(cmd, check=True, text=True)
        print("\n✅ Entorno de tablas preparado correctamente.\n")
        return True
    except subprocess.CalledProcessError:
        print("\n⚠️  Error preparando el entorno de tablas.\n")
        return True
    except Exception as e:
        print(f"\n⚠️  No se pudo preparar el entorno: {e}\n")
        return True


def restaurar_entorno_tablas(nombre_prueba):
    """Ejecuta el script para restaurar los datos al finalizar la prueba."""
    ruta_script = os.path.join(os.path.dirname(__file__), "mosaic_table_manager.py")
    ruta_setups = os.path.join(os.path.dirname(__file__), "set_up_tests", nombre_prueba)

    if not os.path.isdir(ruta_setups):
        return

    print(f"\n🔁 Restaurando entorno original de tablas para '{nombre_prueba}'...\n")

    mostrar_datos = session_state.get_mostrar_datos_tablas()
    cmd = ["python", ruta_script, nombre_prueba, "--restore"]
    if mostrar_datos:
        cmd.append("--mostrar")

    try:
        subprocess.run(cmd, check=True, text=True)
        print("\n✅ Entorno de tablas restaurado correctamente.\n")
    except Exception as e:
        print(f"\n⚠️  No se pudo restaurar el entorno: {e}\n")


def ejecutar_test(ruta_test, nombre_legible):
    """Ejecuta un archivo AHK y controla tablas y simuladores."""
    limpiar_consola(ENCABEZADO_PRUEBAS)
    print(f"🧪 Ejecutando {nombre_legible}...\n")

    nombre_prueba = os.path.splitext(os.path.basename(ruta_test))[0]
    tiene_setup = preparar_entorno_tablas(nombre_prueba)

    # 🔹 Logs de control de simuladores
    usar_simulador = session_state.get_usar_simulador()
    log_info(f"Estado de usar_simulador: {usar_simulador}")

    if usar_simulador:
        print("🧩 El modo simulador está ACTIVADO. Intentando iniciar simuladores...\n")
        try:
            simulators_manager.iniciar_simuladores(nombre_prueba)
            log_info("Simuladores iniciados correctamente (llamada exitosa).")
        except Exception as e:
            log_error(f"Error al intentar iniciar simuladores: {e}")
            print(f"❌ Error al iniciar simuladores: {e}")
    else:
        print("ℹ️  Modo simulador NO activado. Se ejecutará sin simuladores.\n")

    # 🔹 Ejecución de la prueba AHK
    try:
        proceso = subprocess.run(
            ["AutoHotkey.exe", ruta_test],
            capture_output=True,
            text=True
        )
        print("\n⏳ Esperando que finalice la prueba...\n")
        time.sleep(1)

        if proceso.returncode == 0:
            print(f"✅ Prueba '{nombre_legible}' finalizada correctamente.")
        else:
            print(f"⚠️  La prueba '{nombre_legible}' terminó con errores.")
            if proceso.stdout:
                print("\n---- Salida STDOUT ----")
                print(proceso.stdout)
            if proceso.stderr:
                print("\n---- Salida STDERR ----")
                print(proceso.stderr)

    except FileNotFoundError:
        print("❌ No se encontró AutoHotkey.exe en el PATH del sistema.")
        print("Instálelo o agregue su ruta a las variables de entorno.")
    except Exception as e:
        print(f"❌ Error al ejecutar la prueba: {e}")
        log_error(str(e))

    if tiene_setup:
        restaurar_entorno_tablas(nombre_prueba)

    input("\nPresione ENTER para volver al menú de pruebas...")


def menu_pruebas():
    """Menú principal de pruebas automáticas."""
    limpiar_consola(ENCABEZADO_PRUEBAS)

    if not es_administrador():
        print("⚠️  Este módulo requiere permisos de administrador.")
        input("\nPresione ENTER para volver al menú principal...")
        return

    tests = obtener_lista_tests()
    if not tests:
        print("⚠️  No se encontraron scripts de prueba válidos (.ahk) en la carpeta /tests/codes/.")
        input("\nPresione ENTER para volver al menú principal...")
        return

    opciones = [nombre for nombre, _ in tests]

    while True:
        limpiar_consola(ENCABEZADO_PRUEBAS)
        opcion = mostrar_menu("MENÚ DE PRUEBAS AUTOMÁTICAS", opciones)

        if opcion == 0:  # Volver / Salir
            break

        idx = opcion - 1
        _, ruta_test = tests[idx]
        nombre_legible = opciones[idx]
        ejecutar_test(ruta_test, nombre_legible)
