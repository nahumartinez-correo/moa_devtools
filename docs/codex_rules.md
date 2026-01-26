# Reglas operativas para Codex (moa_devtools)

Este documento establece las reglas obligatorias para cualquier trabajo realizado por Codex en este repositorio. Su cumplimiento es mandatorio.

---

## 1) Idioma, tono y estilo

- Todo el trabajo debe realizarse en **español**.
- El tono debe ser **formal**.
- En **comentarios** y en **mensajes de commits** se debe utilizar **voz pasiva con “se …”**.
- No se deben introducir cambios cosméticos ni “mejoras” no solicitadas.

---

## 2) Estrategia de ramas

- Se debe partir siempre desde la rama indicada por el pedido (típicamente `develop*`).
- El trabajo debe realizarse en una rama `mod*` (por ejemplo, `mod0011`), creada desde la rama base indicada si no existiera.
- No se debe mergear a `main` (ni a otras ramas) salvo instrucción explícita.

---

## 3) Convención de commits

- Todos los commits deben estar en español, tono formal y voz pasiva con “se …”.
- Formato obligatorio del mensaje:
  - `modXXXX - Se hace <descripción>`
- Se recomienda granularidad razonable: commits pequeños, con propósito claro y relacionado al alcance.

---

## 4) Restricción crítica: prohibidos los cambios cosméticos

- No se deben modificar **acentos, tildes, signos**, ni “corregir” redacción de comentarios existentes.
- No se debe normalizar **encoding**, ni cambiar saltos de línea, ni aplicar autoformateos masivos.
- No se deben “limpiar” imports, reordenar código o renombrar símbolos si no es necesario para el objetivo.
- No se deben modificar archivos no relacionados al alcance del pedido.

Motivo operativo: cambios de acentos/encoding han provocado fallos posteriores en comandos y en el pipeline de trabajo.

---

## 5) Regla de alcance y estabilidad (especial AHK / pruebas UI)

- En scripts AHK:
  - Se deben mantener **tiempos de espera, coordenadas y focos de ventana** tal como estaban, salvo que el cambio solicitado obligue a moverlos.
  - Se debe preservar la secuencia estable del flujo; si se separan scripts (por ejemplo, “Levantar Mosaic” y flujo de venta), se debe evitar duplicación de pasos (no re-levantar RT ni re-abrir caja si ya se asume el estado).
- Si el pedido incluye eliminación de componentes obsoletos (por ejemplo, referencias a “browser”), se deben remover **todas** las referencias y acciones relacionadas, sin dejar TODOs.

---

## 6) Runner / harness de pruebas

- Si el cambio impacta la forma de ejecución de pruebas, se debe actualizar el runner/harness existente para:
  - Permitir ejecutar cada script de forma individual cuando aplique.
  - Permitir ejecución encadenada cuando sea el caso principal (por ejemplo, Script 1 → Script 2).
- No se debe reintroducir lógica histórica que ya fue desactivada (por ejemplo, levantado de Python inicial si quedó obsoleto).

---

## 7) Verificación mínima antes de entregar

- Se debe validar, como mínimo:
  - que no existan errores de sintaxis,
  - que no se hayan roto includes/rutas,
  - que no existan referencias inexistentes introducidas por el cambio,
  - que el flujo esperado se pueda ejecutar según el runner/harness actualizado (cuando aplique).

---

## 8) Entrega y reporte final

- Se debe dejar un resumen final, incluyendo:
  - lista de archivos modificados/creados,
  - qué se eliminó (por ejemplo, referencias a `browser`),
  - cómo ejecutar el flujo completo y cada parte (comandos/rutas esperadas),
  - notas operativas relevantes (supuestos técnicos, dependencias).

---

## 9) Estructura del proyecto y funcionamiento por módulos

- `main.py`: punto de entrada principal y orquestación de alto nivel.
- `compiler/`: núcleo de compilación y gestión de sesiones, cambios y versiones.
  - Se concentra la lógica de compilación, parches de includes, restauración y operaciones vinculadas al control de versiones.
- `config/`: configuración de sesiones, simuladores y conmutación de parámetros.
  - Se centralizan estados y configuraciones para la ejecución consistente.
- `simulators/`: simuladores y su menú de ejecución.
  - Se agrupan implementaciones y respuestas específicas de simulación.
- `tests/`: runner de pruebas y recursos asociados.
  - Se incluyen scripts AHK de prueba y datos para escenarios configurados.
- `utils/`: utilidades transversales (logging, menús, permisos, servicios).
  - Se proveen servicios comunes reutilizables por el resto de módulos.

---

## 10) Pedidos “solo análisis” (si aplica)

- Si se solicita explícitamente “análisis sin cambios”, no se deben realizar modificaciones ni commits.
- Se debe entregar únicamente un informe técnico con hallazgos y trazabilidad (archivos/funciones/tablas involucradas).
