"""Abstracciones de control de versiones para el compilador.

Provee una interfaz mínima y dos implementaciones: SVN y Git.
La selección de backend se realiza según la versión de MOA
(Vxx.yy), usando SVN para versiones anteriores a V47.09 y
Git para V47.09 en adelante.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional

from utils.logger import log_error, log_info


class VCSBackend:
    """Interfaz mínima de operaciones de control de versiones."""

    def list_modified_files(
        self, base_path: Path | str, exclude_ext: Optional[Iterable[str]] = None
    ) -> List[str]:
        raise NotImplementedError

    def revert_files(
        self, paths: Iterable[str | Path], repo_root: Optional[str | Path] = None
    ) -> None:
        raise NotImplementedError


class SVNBackend(VCSBackend):
    """Backend que encapsula la interacción con SVN."""

    def list_modified_files(
        self, base_path: Path | str, exclude_ext: Optional[Iterable[str]] = None
    ) -> List[str]:
        base = Path(base_path)
        cmd = ["svn", "status", str(base)]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8", check=False
            )
        except FileNotFoundError:
            log_error("SVN no está instalado o no se encuentra en el PATH.")
            return []

        salida = result.stdout.strip().splitlines()
        exclude_ext = {ext.lower() for ext in (exclude_ext or [])}

        modificados = []
        for linea in salida:
            if not linea:
                continue

            if linea[0] not in {"M", "A", "D", "R"}:
                continue

            partes = linea.split(maxsplit=1)
            if len(partes) != 2:
                continue

            ruta_rel = partes[1].strip()

            if any(ruta_rel.lower().endswith(ext) for ext in exclude_ext):
                continue

            modificados.append(ruta_rel.replace("/", "\\"))

        archivos_con_fechas: list[tuple[str, float]] = []
        for rel in modificados:
            ruta_abs = base / rel
            if ruta_abs.exists():
                archivos_con_fechas.append((rel, ruta_abs.stat().st_mtime))

        archivos_con_fechas.sort(key=lambda x: x[1], reverse=True)
        return [a[0] for a in archivos_con_fechas]

    def revert_files(
        self, paths: Iterable[str | Path], repo_root: Optional[str | Path] = None
    ) -> None:
        for path in paths:
            subprocess.run(
                ["svn", "revert", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )


class GitBackend(VCSBackend):
    """Backend que encapsula la interacción con Git."""

    def list_modified_files(
        self, base_path: Path | str, exclude_ext: Optional[Iterable[str]] = None
    ) -> List[str]:
        base = Path(base_path).resolve()
        exclude_ext = {ext.lower() for ext in (exclude_ext or [])}

        repo_root = self._get_repo_root(base)
        if not repo_root:
            return []

        rel_base = base.relative_to(repo_root)
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo_root),
                    "status",
                    "--porcelain",
                    "--untracked-files=all",
                    str(rel_base),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
        except FileNotFoundError:
            log_error("Git no está instalado o no se encuentra en el PATH.")
            return []
        except subprocess.CalledProcessError as exc:
            log_error(
                f"No se pudo obtener el estado de Git en {repo_root}: {exc.stderr or exc}"
            )
            return []

        modificados: list[str] = []
        for linea in result.stdout.strip().splitlines():
            if len(linea) < 4:
                continue

            estado = linea[:2].strip()
            if not estado:
                continue

            resto = linea[3:]
            if " -> " in resto:
                resto = resto.split(" -> ", maxsplit=1)[-1]

            ruta_relativa = Path(resto)
            try:
                ruta_relativa = ruta_relativa.relative_to(rel_base)
            except ValueError:
                continue

            if any(ruta_relativa.as_posix().lower().endswith(ext) for ext in exclude_ext):
                continue

            modificados.append(str(ruta_relativa).replace("/", "\\"))

        archivos_con_fechas: list[tuple[str, float]] = []
        for rel in modificados:
            ruta_abs = base / rel.replace("\\", os.sep)
            if ruta_abs.exists():
                archivos_con_fechas.append((rel, ruta_abs.stat().st_mtime))

        archivos_con_fechas.sort(key=lambda x: x[1], reverse=True)
        return [a[0] for a in archivos_con_fechas]

    def revert_files(
        self, paths: Iterable[str | Path], repo_root: Optional[str | Path] = None
    ) -> None:
        rutas = [str(Path(p)) for p in paths]
        if not rutas:
            return

        root = self._get_repo_root(Path(repo_root) if repo_root else Path.cwd())
        if not root:
            return

        try:
            subprocess.run(
                ["git", "-C", str(root), "restore", "--", *rutas],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except FileNotFoundError:
            log_error("Git no está instalado o no se encuentra en el PATH.")
            return
        except subprocess.CalledProcessError:
            # Intentar compatibilidad con versiones antiguas
            try:
                subprocess.run(
                    ["git", "-C", str(root), "checkout", "--", *rutas],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError as exc:
                log_error(f"No se pudieron revertir archivos con Git: {exc}")

    def _get_repo_root(self, base_path: Path) -> Optional[Path]:
        try:
            result = subprocess.run(
                ["git", "-C", str(base_path), "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
        except FileNotFoundError:
            log_error("Git no está instalado o no se encuentra en el PATH.")
            return None
        except subprocess.CalledProcessError as exc:
            log_error(
                f"El directorio {base_path} no es un repositorio Git válido: {exc.stderr or exc}"
            )
            return None

        ruta = Path(result.stdout.strip()).resolve()
        return ruta if ruta.exists() else None


def _parse_version(version_str: str) -> tuple[int, int]:
    match = re.fullmatch(r"V(\d+)\.(\d+)", version_str.strip(), flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Versión inválida: {version_str}")
    return int(match.group(1)), int(match.group(2))


def get_vcs_backend_for_version(version_str: str) -> VCSBackend:
    """Selecciona el backend de control de versiones según la versión."""

    major, minor = _parse_version(version_str)
    if (major, minor) >= (47, 9):
        log_info(f"Usando backend Git para versión {version_str}.")
        return GitBackend()

    log_info(f"Usando backend SVN para versión {version_str}.")
    return SVNBackend()
