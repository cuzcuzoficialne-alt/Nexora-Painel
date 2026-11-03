"""Gerencia o llama-server local e encaminha chamadas para sua API OpenAI-compatible."""
from __future__ import annotations
import os, shutil, subprocess, threading, time, json, urllib.request, urllib.error
from pathlib import Path
from .config import ROOT, load

_lock = threading.RLock()
_process: subprocess.Popen | None = None
_loaded_path: str | None = None
ENGINE_PORT = int(os.environ.get('NEXORA_ENGINE_PORT', '8001'))


def find_server() -> str | None:
    candidates = [
        shutil.which('llama-server'),
        str(ROOT / '.nexora-runtime' / 'llama.cpp' / 'build' / 'bin' / 'llama-server'),
        str(ROOT / '.nexora-runtime' / 'llama.cpp' / 'build' / 'bin' / 'llama-server.exe'),
        str(ROOT / '.nexora-runtime' / 'llama.cpp' / 'build' / 'bin' / 'Release' / 'llama-server.exe'),
    ]
    return next((p for p in candidates if p and Path(p).is_file()), None)


def _request(path: str, payload=None, timeout=3):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f'http://127.0.0.1:{ENGINE_PORT}{path}', data=data,
        headers={'Content-Type':'application/json'} if data is not None else {})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def is_ready() -> bool:
    try:
        _request('/health', timeout=1)
        return True
    except Exception:
        return False


def start(path: str, model_id: str = 'nexora-local'):
    global _process, _loaded_path
    model = Path(path).expanduser().resolve()
    if not model.is_file() or model.suffix.lower() != '.gguf':
        raise RuntimeError('O caminho selecionado não aponta para um arquivo GGUF válido.')
    with _lock:
        if _process and _process.poll() is None and _loaded_path == str(model) and is_ready():
            return
        stop()
        binary = find_server()
        if not binary:
            raise RuntimeError('llama-server não encontrado. Use a opção 5 para compilar/instalar o motor NEXORA.')
        cfg = load()
        command = [binary, '-m', str(model), '--host', '127.0.0.1', '--port', str(ENGINE_PORT),
                   '--ctx-size', str(int(cfg.get('context_size', 2048))), '--alias', model_id, '-ngl', '0']
        log = (ROOT / 'data' / 'llama-server.log').open('a', encoding='utf-8')
        kwargs = {'cwd': str(Path(binary).parent), 'stdout': log, 'stderr': subprocess.STDOUT}
        if os.name == 'nt': kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        _process = subprocess.Popen(command, **kwargs)
        _loaded_path = str(model)
        deadline = time.time() + 180
        while time.time() < deadline:
            if _process.poll() is not None:
                raise RuntimeError('llama-server encerrou durante a inicialização. Consulte data/llama-server.log.')
            if is_ready(): return
            time.sleep(.5)
        stop()
        raise RuntimeError('Tempo esgotado aguardando o modelo carregar. Reduza o contexto ou escolha um modelo menor.')


def stop():
    global _process, _loaded_path
    with _lock:
        if _process and _process.poll() is None:
            _process.terminate()
            try: _process.wait(timeout=10)
            except subprocess.TimeoutExpired: _process.kill()
        _process = None
        _loaded_path = None


def chat(path, messages, model_id='nexora-local', **options):
    start(path, model_id)
    payload = {'model': model_id, 'messages': messages,
               'temperature': float(options.get('temperature', 0.7)),
               'max_tokens': int(options.get('max_tokens', 512)),
               'stream': False}
    try:
        return _request('/v1/chat/completions', payload, timeout=600)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors='replace')[:1000]
        raise RuntimeError(f'llama-server respondeu HTTP {exc.code}: {detail}') from exc
