from pathlib import Path
import json, secrets
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'; MODELS=ROOT/'models'; BACKUPS=ROOT/'backups'
CONFIG=DATA/'config.json'
DEFAULT={"port":8000,"host":"127.0.0.1","api_key":"","default_model":"","model_path":"","public_tunnel":False,"context_size":2048,"engine_port":8001}
def load():
    DATA.mkdir(exist_ok=True); MODELS.mkdir(exist_ok=True); BACKUPS.mkdir(exist_ok=True)
    if not CONFIG.exists(): save(DEFAULT.copy())
    try: d=json.loads(CONFIG.read_text(encoding='utf-8'))
    except Exception: d={}
    result=DEFAULT.copy(); result.update(d)
    if not result.get('api_key'): result['api_key']='nx-'+secrets.token_urlsafe(30); save(result)
    return result
def save(d):
    DATA.mkdir(exist_ok=True); CONFIG.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
