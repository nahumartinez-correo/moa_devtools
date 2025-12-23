import subprocess
from pathlib import Path

import pytest

from compiler.vcs_backend import (
    GitBackend,
    SVNBackend,
    get_vcs_backend_for_version,
)


def test_backend_selection_threshold():
    assert isinstance(get_vcs_backend_for_version("V46.10"), SVNBackend)
    assert isinstance(get_vcs_backend_for_version("V47.09"), GitBackend)
    assert isinstance(get_vcs_backend_for_version("V48.00"), GitBackend)


def test_git_status_parsing_filters_and_excludes(tmp_path: Path):
    repo_root = tmp_path
    subprocess.run(["git", "init"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL)

    version_src = repo_root / "V47.10" / "src"
    version_src.mkdir(parents=True)

    code_file = version_src / "code1.c"
    header_file = version_src / "header.h"
    outside_file = repo_root / "otro.txt"

    code_file.write_text("print('hola')\n", encoding="utf-8")
    header_file.write_text("// header\n", encoding="utf-8")
    outside_file.write_text("fuera\n", encoding="utf-8")

    backend = GitBackend()
    modificados = backend.list_modified_files(version_src, exclude_ext=[".h"])

    assert "code1.c" in modificados
    assert not any("header.h" in m for m in modificados)
    assert not any("otro.txt" in m for m in modificados)


def test_git_status_ignores_paths_outside_version(tmp_path: Path):
    repo_root = tmp_path
    subprocess.run(["git", "init"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL)

    version_src = repo_root / "V47.10" / "src"
    other_dir = repo_root / "V47.10" / "docs"
    version_src.mkdir(parents=True)
    other_dir.mkdir(parents=True)

    file_inside = version_src / "cambio.c"
    file_outside = other_dir / "nota.txt"

    file_inside.write_text("cambio\n", encoding="utf-8")
    file_outside.write_text("nota\n", encoding="utf-8")

    backend = GitBackend()
    modificados = backend.list_modified_files(version_src, exclude_ext=[".h"])

    assert "cambio.c" in modificados
    assert not any("nota.txt" in m for m in modificados)
