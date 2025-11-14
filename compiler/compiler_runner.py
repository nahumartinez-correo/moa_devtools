import os
import subprocess
from utils.logger import log_info, log_error
from compiler import includes_manager
from utils import service_manager

# ================================================================
# 🔧 Configuración general
# ================================================================
COMANDO_BC = r'bc -npost -s -v -Ic:\moa\src\include'

CARPETAS_NO_COMPILABLES = {"appl", "bit", "pat", "pic", "tag"}

COMPILADORES_ESPECIALES = {
    "fld": r"impfld -npost C:\moaproj\V47.09\src\POST\fld",
    "dsc": r"impdsc -npost C:\moaproj\V47.09\src\POST\dsc",
    "plb": r"imppbl -npost C:\moaproj\V47.09\src\POST\plb",
}

# ================================================================
# 🧠 Función principal
# ================================================================
def compilar_archivo(ruta):
    """Compila un archivo o módulo del proyecto POST, manejando casos especiales."""

    modulo = os.path.basename(os.path.dirname(ruta)).lower()
    base = os.path.basename(ruta).lower()
    extension = os.path.splitext(ruta)[1].lower().lstrip('.')

    # Detectar versión para actualizador de includes
    version = includes_manager._obtener_version_desde_ruta(ruta)

    print(f"\n🧩 Preparando compilación del módulo: {modulo}")
    print(f"📄 Archivo o carpeta: {ruta}\n")

    modificados = []

    try:
        # ================================================================
        # Paso 1: detener servicios
        # ================================================================
        service_manager.detener_todos()

        # ================================================================
        # Paso 2: actualizar includes generales
        # ================================================================
        modificados = includes_manager.actualizar_includes(ruta)

        # ================================================================
        # Paso 3: actualizar include particular del módulo
        # ================================================================
        includes_manager.actualizar_include_modulo(ruta)

        # ================================================================
        # Paso 4: determinar tipo de compilación
        # ================================================================
        comando = None
        clave = None

        # Caso especial: carpeta o extensión especial
        if base in COMPILADORES_ESPECIALES or extension in COMPILADORES_ESPECIALES:
            clave = base if base in COMPILADORES_ESPECIALES else extension
            comando = COMPILADORES_ESPECIALES[clave]
            print(f"\n🧩 Compilando módulo especial: {clave.upper()}")
        else:
            # Compilación normal
            if modulo in CARPETAS_NO_COMPILABLES:
                print(f"⚠ El módulo {modulo.upper()} no está disponible para compilar desde el script.")
                log_info(f"Intento de compilación en módulo no soportado: {modulo}")
                return False

            comando = f'{COMANDO_BC} "{ruta}"'
            clave = "normal"
            print("\n🚧 Ejecutando compilador BC...")

        print(f"💻 Comando: {comando}\n")
        log_info(f"Iniciando compilación ({clave}) con comando: {comando}")

        # ================================================================
        # Paso 5: ejecutar compilación
        # ================================================================
        process = subprocess.Popen(
            comando,
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
            print(f"\n✅ Compilación ({clave}) finalizada correctamente.\n")
            log_info(f"Compilación exitosa ({clave}) para {ruta}")
        else:
            print(f"\n❌ Error durante compilación ({clave}).\n")
            log_error(f"Error en compilación ({clave}) de {ruta}")

    except Exception as e:
        log_error(f"Error en compilación: {e}")
        print(f"\n❌ Error inesperado durante la compilación: {e}\n")

    finally:
        # ================================================================
        # Paso 6: restaurar includes y servicios
        # ================================================================
        includes_manager.restaurar_includes(modificados)
        service_manager.iniciar_todos()
        print("Includes restaurados y servicios reiniciados.\n")


# ================================================================
# 🔍 Ejemplo de uso
# ================================================================
if __name__ == "__main__":
    ruta_prueba = r"C:\moaproj\V47.09\src\POST\fld"
    compilar_archivo(ruta_prueba)
