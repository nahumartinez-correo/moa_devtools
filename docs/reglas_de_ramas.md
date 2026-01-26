# Reglas de ramas de feature (`modNNNN-*`) – moa_devtools

Este documento describe la convención para nombrar y trabajar con ramas de feature en este repositorio.

## Ramas principales del repositorio

- `master`: rama principal, debe reflejar el estado productivo con las features ya validadas en desarrollo.
- `developCompiler`: rama base para todo lo relacionado con el módulo del compilador.
- `developConfig`: rama base para todo lo relacionado con el módulo de configuración del proyecto.
- `developSimulators`: rama base para todo lo relacionado con el módulo de simuladores usados en el proyecto.
- `developTests`: rama base para todo lo relacionado con las pruebas automáticas del proyecto.

Estas ramas son las **únicas** que pueden fusionarse directamente en `master` y siempre mediante el flujo de revisión definido por el equipo.

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

Cada rama de feature se crea a partir de la rama de desarrollo indicada por el alcance, nunca directamente desde `master`:

- Para tareas del módulo compilador:
  - Rama base: `developCompiler`
  - Alcance típico:
    - cambios en `compiler/`,
    - ajustes vinculados a flujo de compilación.
- Para tareas del módulo de configuración:
  - Rama base: `developConfig`
  - Alcance típico:
    - cambios en `config/`,
    - ajustes de estados o parámetros de configuración.
- Para tareas del módulo de simuladores:
  - Rama base: `developSimulators`
  - Alcance típico:
    - cambios en `simulators/`,
    - ajustes en códigos de simulación asociados.
- Para tareas del módulo de pruebas:
  - Rama base: `developTests`
  - Alcance típico:
    - cambios en `tests/`,
    - ajustes en runners y recursos de pruebas.

Si el pedido especifica otra rama base `develop*`, esa rama debe utilizarse como origen.

En ningún caso se crean ramas `modNNNN-*` directamente desde `master`.

## Flujo recomendado para crear una rama de feature

1. Actualizar la rama base local adecuada:

   - Para compilador:
     - `git checkout developCompiler`
     - `git pull origin developCompiler`
   - Para configuración:
     - `git checkout developConfig`
     - `git pull origin developConfig`
   - Para simuladores:
     - `git checkout developSimulators`
     - `git pull origin developSimulators`
   - Para pruebas:
     - `git checkout developTests`
     - `git pull origin developTests`

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

Después de fusionar cambios en `master`, se recomienda actualizar las ramas de desarrollo para mantenerlas alineadas:

`git fetch`
`git checkout master`
`git pull`

`git checkout developCompiler`
`git merge master`
`git push`

`git checkout developConfig`
`git merge master`
`git push`

`git checkout developSimulators`
`git merge master`
`git push`

`git checkout developTests`
`git merge master`
`git push`
