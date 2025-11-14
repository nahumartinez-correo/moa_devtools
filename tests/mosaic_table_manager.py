import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETUP_DIR = os.path.join(BASE_DIR, "set_up_tests")


def log(msg, tipo="info"):
    prefix = {
        "info": "ℹ️ ",
        "ok": "✅ ",
        "warn": "⚠️ ",
        "err": "❌ ",
        "title": "\n" + "=" * 70 + "\n",
    }.get(tipo, "")
    print(f"{prefix}{msg}")


def run_ql(commands: str, server: str):
    """Ejecuta comandos QL contra el servidor indicado."""
    QL_EXEC = ["ql", "-npost", f"-S{server}"]
    result = subprocess.run(
        QL_EXEC,
        input=commands,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.stdout.strip(), result.stderr.strip()


def mostrar_tabla(tabla: str, titulo: str, server: str, mostrar_datos: bool):
    """Muestra el contenido de una tabla si mostrar_datos=True."""
    log(f"\n📋 {titulo} ({tabla})")
    out, err = run_ql(f"select * from {tabla};\n", server)
    if mostrar_datos:
        if err:
            log(f"⚠️ Error consultando tabla: {err}", "warn")
        else:
            print(out)
    else:
        if "records read" in out:
            try:
                # Extraer cantidad de registros del final de la salida
                parts = [x for x in out.splitlines() if "records read" in x]
                if parts:
                    log(f"📊 {parts[-1].strip()}", "info")
            except Exception:
                log("📊 Consulta ejecutada.", "info")
    print("-" * 70)


def preparar_entorno(nombre_prueba: str, mostrar_datos: bool):
    log("======================================================================", "title")
    log("      🧠 MOSAIC TABLE MANAGER - Preparando entorno de prueba")
    log("======================================================================", "title")

    ruta_prueba = os.path.join(SETUP_DIR, nombre_prueba)
    if not os.path.isdir(ruta_prueba):
        log(f"No se encontró la carpeta de configuración para la prueba '{nombre_prueba}'", "err")
        sys.exit(1)

    archivos_tablas = [f for f in os.listdir(ruta_prueba) if f.startswith("table_")]
    if not archivos_tablas:
        log("No se encontraron archivos de tablas para configurar.", "warn")
        return

    for archivo in archivos_tablas:
        tabla = os.path.splitext(archivo[len("table_"):])[0]
        ruta_tabla = os.path.join(ruta_prueba, archivo)
        ruta_backup = os.path.join(ruta_prueba, f"{tabla}.dmp")

        # Leer servidor desde la primera línea
        with open(ruta_tabla, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        server = lineas[0].strip()
        if server not in ("main", "gene"):
            log(f"⚠️ Servidor no válido en {archivo}. Se usará 'main' por defecto.", "warn")
            server = "main"
        # Crear archivo temporal sin la primera línea
        datos_temporales = ruta_tabla + ".tmp"
        with open(datos_temporales, "w", encoding="utf-8") as f:
            f.writelines(lineas[1:])

        log(f"\n📦 Generando backup temporal de la tabla '{tabla}' en servidor '{server}'...")

        # Backup
        commands = f'select from {tabla} dump into "{ruta_backup}";\n'
        out, err = run_ql(commands, server)

        if ("Redirection completed" in out) or ("Output redirected" in out):
            log(f"✅ Backup temporal generado correctamente en: {ruta_backup}", "ok")
        else:
            log(f"⚠️ Posible error en backup de {tabla}.", "warn")

        mostrar_tabla(tabla, "Contenido original de la tabla", server, mostrar_datos)

        # Borrar contenido
        log(f"🧹 Limpiando tabla '{tabla}'...")
        out, err = run_ql(f"delete from {tabla};\n", server)
        if "deleted" in out.lower() or "deleted" in err.lower():
            log("✅ Tabla vaciada correctamente.", "ok")
        else:
            log(f"⚠️ Resultado al limpiar: {out or err}", "warn")

        # Insertar nuevos datos
        log(f"📥 Cargando nuevos datos para la tabla '{tabla}' desde {ruta_tabla} ...")
        out, err = run_ql(f'insert into {tabla} from "{datos_temporales}";\n', server)
        if "Inserted" in out or "Inserted" in err:
            log("✅ Nuevos datos insertados correctamente.", "ok")
        else:
            log(f"⚠️ Resultado del insert:\n{out or err}", "warn")

        mostrar_tabla(tabla, "Contenido de la tabla después de cargar datos del setup", server, mostrar_datos)

        try:
            os.remove(datos_temporales)
        except Exception:
            pass

        time.sleep(0.3)

    log("\n✅ Preparación del entorno de pruebas finalizada correctamente.")


def restaurar_entorno(nombre_prueba: str, mostrar_datos: bool):
    log("======================================================================", "title")
    log(f"       🔁 RESTAURANDO ENTORNO ORIGINAL - {nombre_prueba}")
    log("======================================================================", "title")

    ruta_prueba = os.path.join(SETUP_DIR, nombre_prueba)
    if not os.path.isdir(ruta_prueba):
        log(f"No se encontró la carpeta de configuración para la prueba '{nombre_prueba}'", "err")
        return

    backups = [f for f in os.listdir(ruta_prueba) if f.endswith(".dmp")]
    if not backups:
        log("No se encontraron archivos de backup para restaurar.", "warn")
        return

    for backup in backups:
        tabla = os.path.splitext(backup)[0]
        ruta_backup = os.path.join(ruta_prueba, backup)

        # Determinar servidor usado leyendo el archivo .txt correspondiente
        ruta_tabla = os.path.join(ruta_prueba, f"table_{tabla}.txt")
        if os.path.exists(ruta_tabla):
            with open(ruta_tabla, "r", encoding="utf-8") as f:
                primera = f.readline().strip()
            server = primera if primera in ("main", "gene") else "main"
        else:
            server = "main"

        log(f"\n🧱 Restaurando tabla '{tabla}' desde backup {backup} en servidor '{server}' ...")

        run_ql(f"delete from {tabla};\n", server)
        out, err = run_ql(f'insert into {tabla} from "{ruta_backup}";\n', server)
        if "Inserted" in out or "Inserted" in err:
            log("✅ Tabla restaurada correctamente.", "ok")
        else:
            log(f"⚠️ Resultado del insert de restauración:\n{out or err}", "warn")

        mostrar_tabla(tabla, "Contenido de la tabla luego del restore", server, mostrar_datos)

        try:
            os.remove(ruta_backup)
            log("🗑️  Backup temporal eliminado.", "ok")
        except Exception as e:
            log(f"⚠️ No se pudo eliminar el backup: {e}", "warn")

    log("\n✅ Restauración de entorno completada correctamente.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python mosaic_table_manager.py <nombre_de_prueba> [--restore] [--mostrar]")
        sys.exit(1)

    nombre_prueba = sys.argv[1]
    modo_restore = "--restore" in sys.argv
    mostrar_datos = "--mostrar" in sys.argv

    if modo_restore:
        restaurar_entorno(nombre_prueba, mostrar_datos)
    else:
        preparar_entorno(nombre_prueba, mostrar_datos)
