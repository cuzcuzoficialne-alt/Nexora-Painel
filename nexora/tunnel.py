"""Gerenciador de Cloudflare Quick Tunnel da NEXORA."""
from __future__ import annotations
import os, re, shutil, subprocess, threading, time
from pathlib import Path

_lock = threading.RLock()
_proc: subprocess.Popen | None = None
_url: str | None = None
_log: str = ''
_started_at: float | None = None


def _reader(proc: subprocess.Popen) -> None:
    global _url, _log
    pattern = re.compile(r'https://[a-z0-9-]+\.trycloudflare\.com', re.I)
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            with _lock:
                _log = (line.strip()[-500:] or _log)
                match = pattern.search(line)
                if match:
                    _url = match.group(0)
    except Exception as exc:
        with _lock: _log = str(exc)[:500]


def status() -> dict:
    global _proc, _url
    with _lock:
        running = _proc is not None and _proc.poll() is None
        if not running:
            _url = None
        return {'running': running, 'url': _url if running else None,
                'api_url': (_url + '/v1/chat/completions') if running and _url else None,
                'log': _log}


def start(port: int = 8000) -> dict:
    global _proc, _url, _log, _started_at
    with _lock:
        if _proc is not None and _proc.poll() is None:
            return status()
        exe = shutil.which('cloudflared') or shutil.which('cloudflared.exe')
        if not exe:
            raise RuntimeError('cloudflared não encontrado. Instale pelo guia oficial: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/')
        _url = None; _log = 'Iniciando Cloudflare Quick Tunnel...'
        creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0) if os.name == 'nt' else 0
        _proc = subprocess.Popen([exe, 'tunnel', '--no-autoupdate', '--url', f'http://127.0.0.1:{int(port)}'],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, bufsize=1, creationflags=creationflags)
        _started_at = time.time()
        threading.Thread(target=_reader, args=(_proc,), daemon=True).start()
    deadline = time.time() + 20
    while time.time() < deadline:
        result = status()
        if result['url']:
            return result
        with _lock:
            if _proc is None or _proc.poll() is not None:
                raise RuntimeError('cloudflared encerrou antes de criar o endereço público. ' + _log)
        time.sleep(.25)
    return status()


def stop() -> dict:
    global _proc, _url, _log
    with _lock:
        proc = _proc
        if proc is None or proc.poll() is not None:
            _proc = None; _url = None
            return {'running': False, 'url': None, 'message': 'Túnel já estava parado.'}
        proc.terminate()
    try: proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.wait(timeout=3)
    with _lock:
        _proc = None; _url = None; _log = 'Túnel encerrado.'
    return {'running': False, 'url': None, 'message': 'Túnel encerrado.'}
