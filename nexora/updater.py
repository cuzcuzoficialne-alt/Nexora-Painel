"""Atualizador GitHub com backup e rollback para a NEXORA."""
from __future__ import annotations
import subprocess
from datetime import datetime
from pathlib import Path
from .config import ROOT, BACKUPS

def _git(*args: str, check: bool = True):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if check and result.returncode:
        raise RuntimeError(result.stdout.strip() or f"git {' '.join(args)} falhou.")
    return result

def update() -> dict:
    if not (ROOT / ".git").exists():
        raise RuntimeError("Esta pasta não é um clone Git. Atualize usando o repositório clonado do GitHub.")

    branch = _git("branch", "--show-current").stdout.strip()
    if not branch:
        raise RuntimeError("HEAD destacado. Entre em uma branch antes de atualizar.")

    status = _git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    if status:
        raise RuntimeError(
            "Há alterações em arquivos versionados. Para não apagar seu trabalho, "
            "a atualização foi cancelada. Faça commit ou guarde suas alterações e tente novamente."
        )

    remote = _git("config", "--get", f"branch.{branch}.remote", check=False)
    merge = _git("config", "--get", f"branch.{branch}.merge", check=False)
    if remote.returncode or merge.returncode or not remote.stdout.strip() or not merge.stdout.strip():
        raise RuntimeError("A branch atual não possui upstream configurado. Configure o rastreamento do GitHub primeiro.")

    old_head = _git("rev-parse", "HEAD").stdout.strip()
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"nexora-update-{stamp}.zip"
    _git("archive", "--format=zip", "-o", str(backup), old_head)

    try:
        _git("fetch", "--prune", remote.stdout.strip())
        target = f"{remote.stdout.strip()}/{merge.stdout.strip().removeprefix('refs/heads/')}"
        ancestor = _git("merge-base", "--is-ancestor", old_head, target, check=False)
        if ancestor.returncode != 0:
            raise RuntimeError("A atualização não é um avanço direto (fast-forward). Nada foi alterado.")
        _git("merge", "--ff-only", target)
        new_head = _git("rev-parse", "HEAD").stdout.strip()
        if new_head == old_head:
            return {"updated": False, "message": "A NEXORA já está atualizada.", "backup": str(backup)}
        return {"updated": True, "message": "Atualização concluída com sucesso.", "backup": str(backup),
                "previous": old_head[:10], "current": new_head[:10]}
    except Exception:
        current = _git("rev-parse", "HEAD", check=False).stdout.strip()
        if current and current != old_head:
            _git("reset", "--hard", old_head, check=False)
        raise
