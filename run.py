#!/usr/bin/env python3
"""Inicializador NEXORA: verifica dependências e prepara o ambiente."""
from __future__ import annotations

import importlib.util
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

ANDROID = (
    sys.platform == "android"
    or "ANDROID_ROOT" in os.environ
    or "com.termux" in os.environ.get("PREFIX", "")
)

REQUIRED_MODULES = (
    "fastapi",
    "uvicorn",
    "h11",
    "click",
    "annotated_doc",
    "annotated_types",
    "typing_inspection",
    "pydantic",
    "pydantic_core",
    "huggingface_hub",
    "requests",
    "filelock",
    "fsspec",
    "packaging",
    "yaml",
    "tqdm",
    "typing_extensions",
    "multipart",
)


def banner() -> None:
    print("\033[95m NEXORA AI • LOCAL INTELLIGENCE • 0.9.1\033[0m")


def run_pip(*args: str) -> bool:
    command = [sys.executable, "-m", "pip", *args]
    print("\n>", " ".join(command))
    return subprocess.run(command, cwd=ROOT).returncode == 0


def prepare_android_pydantic() -> bool:
    """Instala o wheel Android conhecido, evitando compilação Rust no Termux."""
    try:
        import pydantic
        import pydantic_core

        if pydantic.__version__ == "2.14.0" and pydantic_core.__version__ == "2.50.0":
            return True
    except Exception:
        pass

    index = "https://eutalix.github.io/android-pydantic-core/"
    print("Preparando pydantic-core compatível com Android/Termux (Python 3.14)...")
    if not run_pip(
        "install", "--only-binary=:all:", "pydantic-core==2.50.0",
        "--extra-index-url", index,
    ):
        print("Não foi possível obter o wheel Android do pydantic-core.")
        print("Confira Python 3.14, arquitetura suportada e conexão com a internet.")
        return False

    # O par 2.14.0 / 2.50.0 foi validado no Termux Python 3.14 ARM64.
    if not run_pip("install", "--no-deps", "--force-reinstall", "pydantic==2.14.0"):
        return False
    return True


def deps() -> bool:
    print(
        "Sistema:", platform.system(),
        "| Arquitetura:", platform.machine(),
        "| Python:", platform.python_version(),
    )
    if sys.version_info < (3, 10):
        print("Python 3.10 ou superior é necessário.")
        return False

    if ANDROID and sys.version_info >= (3, 14):
        if not prepare_android_pydantic():
            return False

    missing = [
        name for name in REQUIRED_MODULES
        if importlib.util.find_spec(name) is None
    ]
    requirements = ROOT / "requirements.txt"
    if missing:
        print("Dependências ausentes:", ", ".join(missing))
        print("Instalando dependências declaradas em requirements.txt...")
        if not run_pip("install", "-r", str(requirements)):
            print("\\nFalha ao instalar dependências.")
            print("Não use --no-deps: isso deixa dependências internas faltando.")
            return False

    # Importação real: find_spec sozinho não detecta dependências transitivas quebradas.
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        import h11  # noqa: F401
        from huggingface_hub import HfApi, hf_hub_download  # noqa: F401
        import pydantic
        import pydantic_core
        if pydantic.__version__ != "2.14.0" or pydantic_core.__version__ != "2.50.0":
            if ANDROID and sys.version_info >= (3, 14):
                print(
                    "Versões Pydantic inesperadas:",
                    pydantic.__version__, "/", pydantic_core.__version__,
                )
                return False
        print(
            "Dependências verificadas:",
            f"FastAPI {fastapi.__version__},",
            f"Pydantic {pydantic.__version__},",
            f"Core {pydantic_core.__version__},",
            f"h11 {h11.__version__}",
        )
    except Exception as exc:
        print("Falha ao importar dependências:", type(exc).__name__, str(exc))
        print("Tente: python -m pip check")
        return False
    return True


def main() -> None:
    banner()
    if not deps():
        print("\nNão foi possível preparar a NEXORA. Corrija as dependências acima.")
        return
    from nexora.cli import menu
    menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[96mNEXORA\033[0m\n\033[92m✓ Encerramento solicitado. Até a próxima!\033[0m")
