# Reglas de ramas de feature (`modNNNN-*`) – moa_devtools

Este documento describe la convención para nombrar y trabajar con ramas de feature en este repositorio.

## Ramas principales del repositorio

- `main`: rama principal, debe reflejar un estado productivo o cercano a productivo de las herramientas.
- `develop`: rama base para el trabajo de integración general.

Estas ramas son las **únicas** que pueden fusionarse directamente en `main` y siempre mediante el flujo de revisión definido por el equipo.

## Convención general de ramas de feature

- Prefijo obligatorio: `mod`
- Cuatro dígitos: `0001`, `0002`, `0003`, ...
- Sufijo en kebab-case, en español, describiendo de forma corta la intención de la rama.

**Ejemplos:**

- `mod0007-ajustes-compilador`
- `mod0008-simuladores-estado`
- `mod0009-pruebas-runner-ahk`
- `mod0010-configuracion-sesiones`

## Rama base para cada feature

Cada rama de feature se crea a partir de la rama de desarrollo indicada por el pedido, nunca directamente desde `main`:

- Para tareas generales o de integración:
  - Rama base: `develop`
  - Ejemplos de tareas:
    - ajustes en `compiler/`,
    - cambios en `simulators/`,
    - mejoras en `tests/` y runners,
    - actualizaciones en `config/` o `utils/`.

Si el pedido especifica otra rama base (por ejemplo, una rama `develop*` particular), esa rama debe utilizarse como origen.

En ningún caso se crean ramas `modNNNN-*` directamente desde `main`.

## Flujo recomendado para crear una rama de feature

1. Actualizar la rama base local adecuada:

   - Para integración general:
     - `git checkout develop`
     - `git pull origin develop`

2. Identificar el siguiente identificador disponible (`modNNNN`) según el control interno del equipo.

3. Crear la nueva rama de feature con el siguiente identificador libre y una descripción corta en kebab-case:

   Ejemplo:

   `git checkout -b mod0012-documentacion-general`
   `git push -u origin mod0012-documentacion-general`

4. Registrar la nueva rama en el documento interno de historial de ramas, si aplica en el flujo del equipo.

## Actualización del historial de ramas

Cada vez que se crea, fusiona o descarta una rama de feature:

- Se debe actualizar el historial interno de ramas, incluyendo:
  - identificador (`modNNNN`),
  - rama creada,
  - estado (en progreso / fusionada en `main` / descartada),
  - descripción breve del alcance.

## Actualización de ramas de desarrollo tras merge a `main`

Después de fusionar cambios en `main`, se recomienda actualizar `develop` para mantenerla alineada:

`git fetch`
`git checkout main`
`git pull`

`git checkout develop`
`git merge main`
`git push`
