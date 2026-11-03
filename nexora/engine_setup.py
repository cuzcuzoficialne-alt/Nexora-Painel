"""Instala/compila llama.cpp com o alvo llama-server."""
from __future__ import annotations
import os, platform, shutil, subprocess, sys
from pathlib import Path
from .config import ROOT

SOURCE = ROOT / '.nexora-runtime' / 'llama.cpp'

def run(command, cwd=None):
    print('\n>', ' '.join(map(str, command)))
    return subprocess.run(command, cwd=cwd).returncode == 0

def install_engine():
    system = platform.system().lower()
    print(f'Sistema: {platform.system()} | Arquitetura: {platform.machine()}')
    if system == 'android' or 'ANDROID_ROOT' in os.environ or 'com.termux' in os.environ.get('PREFIX',''):
        missing = [x for x in ('git','cmake','clang','make') if not shutil.which(x)]
        if missing:
            print('No Termux, instale as ferramentas necessárias com:')
            print('pkg update && pkg install git cmake clang make libandroid-spawn')
            return False
    else:
        missing = [x for x in ('git','cmake') if not shutil.which(x)]
        if missing:
            print('Instale primeiro estas ferramentas e execute novamente:', ', '.join(missing))
            print('Windows: Git + CMake + Visual Studio Build Tools (C++).')
            print('macOS: xcode-select --install e brew install cmake git.')
            print('Linux: instale git, cmake e compilador C/C++ pelo gerenciador da distribuição.')
            return False
    if not SOURCE.exists():
        SOURCE.parent.mkdir(parents=True, exist_ok=True)
        if not run(['git','clone','--depth','1','https://github.com/ggml-org/llama.cpp',str(SOURCE)]):
            print('Falha ao baixar llama.cpp. Verifique a conexão e tente novamente.')
            return False
    build = SOURCE / 'build'
    configure = ['cmake','-S',str(SOURCE),'-B',str(build),'-DCMAKE_BUILD_TYPE=Release']
    if not run(configure):
        print('Configuração CMake falhou. Verifique as ferramentas de compilação.')
        return False
    jobs = max(1, min(2 if ('ANDROID_ROOT' in os.environ or 'com.termux' in os.environ.get('PREFIX','')) else 4, (os.cpu_count() or 2)-1))
    if not run(['cmake','--build',str(build),'--config','Release','--target','llama-server','--parallel',str(jobs)]):
        print('Compilação falhou. Consulte a saída acima; em celulares, libere RAM e armazenamento.')
        return False
    binary = build / 'bin' / ('llama-server.exe' if os.name == 'nt' else 'llama-server')
    if not binary.exists():
        print('Compilação terminou, mas o executável não foi encontrado:', binary)
        return False
    print('\nMotor instalado com sucesso:', binary)
    return True

if __name__ == '__main__':
    sys.exit(0 if install_engine() else 1)
