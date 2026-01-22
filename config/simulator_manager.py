from utils.menu import mostrar_menu
from utils.logger import log_info, log_error
from utils.permissions import es_administrador
from utils import service_manager
from utils.common import limpiar_consola
from config import switch_config, session_state
from config.diccionarios_updater import actualizar_diccionarios_por_integracion
from config.includes_updater import aplicar_includes, revertir_includes
from config.scripts_runner import ejecutar_initsuc, ejecutar_oper_test
from config.servicios_actions import detener_servicios, iniciar_servicios


def menu_configuracion():
    """Menú principal de configuración de MercadoPago."""
    while True:
        limpiar_consola("MOA DevTools - CONFIGURACIÓN DE SIMULADOR")

        if not es_administrador():
            print("⚠️  No tiene permisos de administrador.")
            print("   Ejecute el script en modo administrador para modificar la configuración.\n")
            input("Presione ENTER para volver al menú principal...")
            return

        opciones = [
            "Detener los servicios",
            "Iniciar los servicios",
            "Ajustar los includes",
            "Revertir los includes",
            "Actualizar diccionarios",
            "Crear sucursal",
            "Crear operador",
            "MercadoPago - Usar simulador",
            "MercadoPago - Usar OpenShift",
            "MercadoPago - Usar PC de Ramiro (IP)",
            "MercadoPago - Usar PC de Ramiro (DNS)"
        ]

        opcion = mostrar_menu("CONFIGURACIÓN DE MERCADOPAGO", opciones)
        if opcion == 0:
            print("\n↩️  Volviendo al menú principal...\n")
            return

        if opcion == 1:
            limpiar_consola("MOA DevTools - SERVICIOS")
            detener_servicios()
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 2:
            limpiar_consola("MOA DevTools - SERVICIOS")
            iniciar_servicios()
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 3:
            limpiar_consola("MOA DevTools - INCLUDES")
            print("Ajustando includes...\n")
            if aplicar_includes():
                print("\nIncludes ajustados correctamente.")
            else:
                print("\nNo fue posible ajustar los includes.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 4:
            limpiar_consola("MOA DevTools - INCLUDES")
            print("Revirtiendo includes...\n")
            if revertir_includes():
                print("\nIncludes revertidos correctamente.")
            else:
                print("\nNo fue posible revertir los includes.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 5:
            limpiar_consola("MOA DevTools - ACTUALIZAR DICCIONARIOS")
            print("Actualizando diccionarios...\n")
            if actualizar_diccionarios_por_integracion():
                print("\nActualización finalizada correctamente.")
            else:
                print("\nLa actualización finalizó con errores.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 6:
            limpiar_consola("MOA DevTools - CREAR SUCURSAL")
            if ejecutar_initsuc():
                print("\nSucursal creada correctamente.")
            else:
                print("\nNo fue posible crear la sucursal.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue
        if opcion == 7:
            limpiar_consola("MOA DevTools - CREAR OPERADOR")
            if ejecutar_oper_test():
                print("\nOperador creado correctamente.")
            else:
                print("\nNo fue posible crear el operador.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue

        limpiar_consola("MOA DevTools - CONFIGURACIÓN DE SIMULADOR")
        seleccion = opciones[opcion - 1]
        print(f"🧩 Configurando entorno para: {seleccion}\n")

        # 🧠 Registrar estado del simulador según la opción elegida
        if opcion == 8:
            session_state.set_usar_simulador(True)
            print("🔹 Variable global: usar_simulador = True")
            log_info("Configurado para usar simulador (session_state actualizado).")
        else:
            session_state.set_usar_simulador(False)
            print("🔹 Variable global: usar_simulador = False")
            log_info("Configurado para NO usar simulador (session_state actualizado).")

        # Verificar valor actual en memoria
        print(f"🔍 Estado actual del flag (get_usar_simulador): {session_state.get_usar_simulador()}")
        print()

        print("🧱 Deteniendo servicio SwitchDemand...\n")
        if not switch_config.detener_servicio("SwitchDemand"):
            print("❌ No se pudo detener el servicio. No se aplicarán los cambios.")
            input("\nPresione ENTER para volver al menú anterior...")
            continue

        print("📝 Modificando archivo SwitchDemand.ini...\n")
        try:
            switch_config.actualizar_configuracion(opcion - 7)
            print("✅ Archivo actualizado correctamente.\n")
            log_info(f"Configuración de MercadoPago actualizada (opción {opcion}).")
        except Exception as e:
            print(f"❌ Error al modificar el archivo: {e}")
            log_error(str(e))
            input("\nPresione ENTER para volver al menú anterior...")
            continue

        print("🚀 Reiniciando servicio SwitchDemand...\n")
        service_manager.iniciar_todos()

        print("\n✅ Cambios aplicados correctamente.")
        print(f"🧠 Estado final del flag 'usar_simulador': {session_state.get_usar_simulador()}")
        input("\nPresione ENTER para volver al menú anterior...")
