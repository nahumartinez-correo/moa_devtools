# Arquitectura de MOA DevTools

Este documento describe la arquitectura técnica de **MOA DevTools**, sus módulos
principales, el flujo de trabajo esperado y las dependencias operativas que se
asumen para ejecutar las herramientas de compilación, configuración, pruebas y
simulación.

------------------------------------------------------------
1. Visión general
------------------------------------------------------------

MOA DevTools es un conjunto de herramientas de consola escritas en **Python**
que centraliza tareas habituales del ecosistema Mosaic/MOA, tales como:

- Compilación de archivos de POST y manejo de includes.
- Configuración de entorno para simuladores y SwitchDemand.
- Ejecución de pruebas automáticas basadas en **AutoHotkey (AHK)**.
- Gestión de simuladores y utilidades auxiliares.

El flujo principal es un menú de consola que orquesta el acceso a cada módulo.
La ejecución se realiza en un entorno Windows con rutas y servicios específicos
al stack de Mosaic/MOA.

------------------------------------------------------------
2. Tecnologías y dependencias operativas
------------------------------------------------------------

La solución está basada en los siguientes componentes:

- **Python** como runtime principal de todas las herramientas.
- **AutoHotkey (AHK)** para automatizar flujos de UI en las pruebas.
- **SVN** para detectar y revertir cambios en archivos de POST.
- **Herramientas de compilación** externas (`bc`, `imp*`) invocadas mediante
  `subprocess`.
- **Servicios de Windows** controlados por `sc` (ej. `SwitchDemand`, `RTBatch`).
- **CLI QL** (`ql`) para preparar y restaurar tablas en pruebas.

Rutas y convenciones clave del entorno:

- Base del proyecto: `C:\moaproj`.
- Logs centralizados: `C:\logs\moa_devtools.log`.
- Archivo de configuración de SwitchDemand: `C:\Program Files\SwitchDemand\SwitchDemand.ini`.

------------------------------------------------------------
3. Punto de entrada y orquestación
------------------------------------------------------------

El archivo `main.py` expone el menú principal del sistema. Desde allí se
redirige a los distintos módulos:

- Compilador.
- Configuración.
- Pruebas automáticas.
- Simuladores.

El menú utiliza utilidades comunes (`utils.menu`, `utils.common`) y valida
permisos de administrador antes de ejecutar acciones sensibles.

------------------------------------------------------------
4. Organización por módulos
------------------------------------------------------------

La estructura del repositorio se divide en módulos funcionales:

- `compiler/`: lógica de compilación, patches de includes y recuperación.
- `config/`: configuración del entorno (servicios, includes, diccionarios).
- `tests/`: ejecución de pruebas AHK y preparación de datos.
- `simulators/`: gestión de simuladores y ejecución por parámetros.
- `utils/`: utilidades transversales (menús, logging, permisos).

### 4.1 Módulo de compilación (`compiler/`)

Responsabilidades principales:

- Detectar archivos modificados en SVN dentro de POST.
- Aplicar reemplazos de includes generales a headers.
- Compilar archivos individuales o en lote.
- Restaurar headers con `svn revert` al finalizar.

Componentes clave:

- `compiler_menu.py`: menú del compilador y flujo completo de trabajo.
- `compiler_core.py`: compilación efectiva y manejo de archivos especiales.
- `include_patcher.py`: reemplazos de includes a nivel general.
- `includes_manager.py`: fuente única de reemplazos literales de includes.
- `restore_manager.py`: revert de headers modificados mediante SVN.
- `svn_changes.py`: detección de cambios en POST vía `svn status`.

Notas operativas:

- La compilación usa `bc` con la ruta de includes global y puede ejecutar
  comandos `imp*` para extensiones especiales.
- El módulo opera sobre versiones ubicadas en `C:\moaproj\Vxx.xx\src`.

### 4.2 Módulo de configuración (`config/`)

Responsabilidades principales:

- Ajustar includes en headers de la rama Mosaic-gitlab.
- Actualizar diccionarios y archivos relacionados con integración.
- Detener/iniciar servicios requeridos para cambios de configuración.
- Modificar parámetros del simulador de SwitchDemand.

Componentes clave:

- `simulator_manager.py`: menú de configuración y opciones de entorno.
- `switch_config.py`: edición del bloque `[port10]` en `SwitchDemand.ini`.
- `diccionarios_updater.py`: actualización de diccionarios y recompilación.
- `includes_updater.py`: aplicar/revertir includes con backup en memoria.
- `servicios_actions.py` y `scripts_runner.py`: acciones auxiliares del módulo.

Notas operativas:

- Se trabaja con rutas fijas de `C:\moaproj` y subdirectorios `post`,
  `Mosaic-gitlab`, `scripts`.
- Se controlan servicios definidos en `config.constants` antes de operaciones
  destructivas o de reemplazo masivo.

### 4.3 Módulo de pruebas (`tests/`)

Responsabilidades principales:

- Ejecutar scripts AHK de pruebas automáticas.
- Preparar y restaurar datos de tablas antes y después de cada test.
- Levantar simuladores asociados a cada prueba cuando aplica.

Componentes clave:

- `ahk_runner.py`: menú y ejecución de pruebas AHK.
- `mosaic_table_manager.py`: preparación y restore de tablas con QL.
- `simulators_manager.py`: arranque de simuladores según `simulators.txt`.

Notas operativas:

- Los scripts AHK se ubican en `tests/codes/`.
- Los setups de tablas se ubican en `tests/set_up_tests/<nombre_prueba>/`.
- Se utiliza un flag global (`config.session_state`) para decidir si se
  levantan simuladores o no.

### 4.4 Módulo de simuladores (`simulators/`)

Responsabilidades principales:

- Enumerar simuladores disponibles según estructura en `simulators/codes/`.
- Ejecutar simuladores con o sin parámetros de condición.
- Abrir procesos en consola separada (Windows) o terminal disponible (Unix).

Componentes clave:

- `simulators_menu.py`: menú de simuladores y selección de condiciones.
- `manager.py`: lógica de descubrimiento y ejecución de simuladores.

Notas operativas:

- Cada simulador debe exponer un entrypoint con el mismo nombre de carpeta.
- Las condiciones se toman del archivo `<simulador>_conditions.py`.

### 4.5 Utilidades transversales (`utils/`)

Responsabilidades principales:

- Menús reutilizables de consola.
- Logging centralizado a archivo.
- Validación de permisos de administrador.
- Control de servicios Windows.

Componentes clave:

- `menu.py`: menú interactivo genérico.
- `logger.py`: escritura de logs en `C:\logs\moa_devtools.log`.
- `permissions.py`: verificación de privilegios de administrador.
- `service_manager.py`: control de servicios `sc`.

------------------------------------------------------------
5. Flujo de trabajo típico
------------------------------------------------------------

Un flujo de trabajo estándar se realiza en los siguientes pasos:

1) **Ingresar al menú principal** y seleccionar el módulo requerido.
2) **Verificar permisos de administrador** cuando el módulo lo exige.
3) **Ejecutar la tarea** (compilar, configurar, probar, simular).
4) **Revertir cambios temporales** cuando aplica:
   - Headers revertidos con `svn revert`.
   - Includes restaurados desde backups en memoria.
   - Datos de tablas restaurados en pruebas.
5) **Reiniciar servicios** si fueron detenidos durante el proceso.

------------------------------------------------------------
6. Cómo se realizan los cambios en el proyecto
------------------------------------------------------------

El repositorio se organiza por módulos, por lo que los cambios se planifican
según el área involucrada:

- Cambios en compilación → `compiler/`.
- Cambios en configuración → `config/`.
- Cambios en pruebas → `tests/`.
- Cambios en simuladores → `simulators/`.
- Utilidades compartidas → `utils/`.

Recomendaciones prácticas:

- Mantener cambios acotados al módulo objetivo.
- Evitar modificaciones cosméticas no solicitadas.
- Verificar que no se rompan rutas o dependencias de herramientas externas.
- Ejecutar el flujo de prueba mínimo cuando el cambio lo requiera.

------------------------------------------------------------
7. Estado y variables compartidas
------------------------------------------------------------

Se utilizan variables globales para coordinar comportamientos entre módulos:

- `config.session_state` guarda flags como:
  - `usar_simulador`: determina si deben iniciarse simuladores en pruebas.
  - `mostrar_datos_tablas`: habilita la impresión de datos en la preparación.

Estos flags se consultan tanto en `tests/` como en `config/` para mantener un
comportamiento consistente durante la sesión de ejecución.

------------------------------------------------------------
8. Logging y trazabilidad
------------------------------------------------------------

El logging se centraliza en el archivo:

- `C:\logs\moa_devtools.log`

Todas las funciones críticas escriben mensajes con timestamp y nivel de log
(Info/Error), lo que permite auditar acciones como:

- Inicio de compilaciones y restauraciones.
- Actualización de diccionarios y includes.
- Detención/inicio de servicios.

------------------------------------------------------------
9. Consideraciones operativas y supuestos
------------------------------------------------------------

- El entorno esperado es Windows con acceso a `C:\moaproj` y servicios Mosaic.
- Las herramientas externas (`bc`, `imp*`, `ql`, `svn`, `AutoHotkey.exe`) deben
  estar disponibles en el PATH o en rutas conocidas.
- Los procesos de simuladores y AHK se ejecutan en consola separada cuando es
  posible, para aislar la ejecución de la herramienta principal.
- Las operaciones de configuración asumen permisos de administrador para
  manipular servicios y archivos de sistema.
