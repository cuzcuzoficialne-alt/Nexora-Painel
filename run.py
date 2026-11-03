#!/usr/bin/env python3
from __future__ import annotations
import os,sys,subprocess,platform,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent; os.chdir(ROOT)
REQUIRED={'fastapi':'fastapi>=0.115,<1','uvicorn':'uvicorn>=0.30,<1','huggingface_hub':'huggingface_hub>=0.25,<1'}
def banner():
 print('\033[95m NEXORA AI • LOCAL INTELLIGENCE • 0.9.0\033[0m')
def deps():
 print('Sistema:',platform.system(),'| Arquitetura:',platform.machine(),'| Python:',platform.python_version())
 if sys.version_info<(3,10): print('Python 3.10+ necessário.'); return False
 missing=[spec for mod,spec in REQUIRED.items() if importlib.util.find_spec(mod) is None]
 if missing:
  print('Instalando dependências ausentes:',', '.join(missing))
  if subprocess.run([sys.executable,'-m','pip','install','--upgrade',*missing]).returncode: return False
 return True
def main():
 banner()
 if not deps(): print('Não foi possível preparar a NEXORA.'); return
 from nexora.cli import menu; menu()
if __name__=='__main__':
 try: main()
 except KeyboardInterrupt: print('\n\033[96mNEXORA\033[0m\n\033[92m✓ Encerramento solicitado. Até a próxima!\033[0m')
