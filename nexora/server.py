from __future__ import annotations
import os, platform, shutil, json, secrets, urllib.request, urllib.error
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .config import load, save, ROOT, MODELS, DATA
from .engine import chat, stop, is_ready, find_server, start
from .models import list_installed, select_model
from . import tunnel as tunnel_manager

VERSION='0.9.1'
app=FastAPI(title='NEXORA AI API',version=VERSION)
WEB=ROOT/'web'; KEY_FILE=DATA/'api_keys.json'; ENGINE_PORT=int(os.environ.get('NEXORA_ENGINE_PORT','8001'))
app.mount('/assets',StaticFiles(directory=WEB),name='assets')
class ModelSelection(BaseModel): filename:str
class SettingsUpdate(BaseModel): context_size:int=Field(ge=512,le=32768); port:int=Field(ge=1024,le=65535)
class KeyCreate(BaseModel): name:str=Field(min_length=1,max_length=50)

def read_keys():
    DATA.mkdir(exist_ok=True)
    try: data=json.loads(KEY_FILE.read_text())
    except Exception: data=[]
    return data if isinstance(data,list) else []
def write_keys(data): KEY_FILE.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
def auth(value):
    token=(value or '').removeprefix('Bearer ').strip()
    if not token: raise HTTPException(401,'Informe Authorization: Bearer nx-...')
    c=load()
    if secrets.compare_digest(token,str(c['api_key'])): return 'master'
    for item in read_keys():
        if item.get('active',True) and secrets.compare_digest(token,str(item.get('key',''))): return item.get('name','API key')
    raise HTTPException(401,'Chave NEXORA inválida ou revogada.')
def engine_request(path,payload):
    c=load()
    if not c.get('model_path'): raise HTTPException(503,'Nenhum modelo selecionado. Instale um modelo pelo menu.')
    try: start(c['model_path'],c.get('default_model') or 'nexora-local')
    except Exception as e: raise HTTPException(503,'Motor indisponível: '+str(e))
    body=json.dumps(payload).encode()
    req=urllib.request.Request(f'http://127.0.0.1:{ENGINE_PORT}{path}',data=body,headers={'Content-Type':'application/json'},method='POST')
    try: return urllib.request.urlopen(req,timeout=900)
    except urllib.error.HTTPError as e: raise HTTPException(e.code,e.read().decode(errors='replace')[:2000])
    except Exception as e: raise HTTPException(503,'Falha ao comunicar com llama-server: '+str(e))
@app.on_event('shutdown')
def shutdown_engine():
    tunnel_manager.stop()
    stop()
@app.get('/')
def home(): return FileResponse(WEB/'index.html')
@app.get('/health')
def health():
    c=load(); return {'status':'ok','model':c.get('default_model') or None,'engine':'llama.cpp','engine_ready':is_ready(),'version':VERSION}
@app.get('/dashboard/status')
def dashboard_status():
    c=load(); usage=shutil.disk_usage(ROOT); ram={'total':None,'available':None}
    try:
        if Path('/proc/meminfo').exists():
            vals={}
            for line in Path('/proc/meminfo').read_text().splitlines():
                k,v=line.split(':',1); vals[k]=int(v.strip().split()[0])*1024
            ram={'total':vals.get('MemTotal'),'available':vals.get('MemAvailable')}
        else:
            import psutil; m=psutil.virtual_memory(); ram={'total':m.total,'available':m.available}
    except Exception: pass
    return {'status':'online','version':VERSION,'os':platform.platform(),'architecture':platform.machine(),'python':platform.python_version(),'model':c.get('default_model') or None,'model_path':c.get('model_path') or None,'engine_installed':bool(find_server()),'engine_ready':is_ready(),'disk':{'total':usage.total,'free':usage.free},'ram':ram,'port':c['port'],'context_size':c['context_size']}
@app.get('/dashboard/models')
def dashboard_models():
    c=load(); return {'models':[{'filename':p.name,'path':str(p.resolve()),'size':p.stat().st_size,'active':str(p.resolve())==str(Path(c.get('model_path') or '').resolve())} for p in list_installed()]}
@app.post('/dashboard/models/select')
def dashboard_select(body:ModelSelection,authorization:str|None=Header(default=None)):
    auth(authorization)
    target=(MODELS/body.filename).resolve()
    if target.parent!=MODELS.resolve() or not target.is_file() or target.suffix.lower()!='.gguf': raise HTTPException(404,'Modelo GGUF não encontrado.')
    stop(); select_model(target); return {'ok':True,'model':target.stem,'message':'Modelo alterado. Será carregado na próxima conversa.'}
@app.get('/dashboard/config')
def dashboard_config():
    c=load(); return {'port':c['port'],'context_size':c['context_size'],'host':c['host']}
@app.put('/dashboard/config')
def dashboard_update_config(body:SettingsUpdate,authorization:str|None=Header(default=None)):
    auth(authorization)
    c=load(); c.update(port=body.port,context_size=body.context_size); save(c); return {'ok':True,'message':'Salvo. A nova porta vale após reiniciar.'}
@app.get('/dashboard/keys')
def keys_list(authorization:str|None=Header(default=None)):
    auth(authorization); return {'keys':[{'id':x['id'],'name':x['name'],'created_at':x['created_at'],'active':x.get('active',True),'last4':x['key'][-4:]} for x in read_keys()]}
@app.post('/dashboard/keys')
def keys_create(body:KeyCreate,authorization:str|None=Header(default=None)):
    auth(authorization); items=read_keys(); key='nx-'+secrets.token_urlsafe(32); item={'id':secrets.token_hex(8),'name':body.name.strip(),'key':key,'created_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'active':True}; items.append(item); write_keys(items); return {'ok':True,'key':key,'id':item['id'],'warning':'Copie agora. A chave completa não será exibida novamente.'}
@app.delete('/dashboard/keys/{key_id}')
def keys_revoke(key_id:str,authorization:str|None=Header(default=None)):
    auth(authorization); items=read_keys(); found=False
    for item in items:
        if item.get('id')==key_id: item['active']=False; found=True
    if not found: raise HTTPException(404,'Chave não encontrada.')
    write_keys(items); return {'ok':True,'message':'Chave revogada.'}
@app.get('/v1/models')
def models(authorization:str|None=Header(default=None)):
    auth(authorization); c=load(); data=[]
    for p in list_installed(): data.append({'id':c.get('default_model') if str(p.resolve())==str(Path(c.get('model_path') or '').resolve()) else p.stem,'object':'model','owned_by':'nexora'})
    return {'object':'list','data':data}
@app.post('/v1/chat/completions')
def chat_completions(body:dict,authorization:str|None=Header(default=None)):
    auth(authorization); c=load(); messages=body.get('messages')
    if not isinstance(messages,list) or not messages: raise HTTPException(400,'Envie messages como uma lista não vazia.')
    if body.get('stream'):
        response=engine_request('/v1/chat/completions',{**body,'model':c.get('default_model') or body.get('model','nexora-local')})
        def chunks():
            try:
                while True:
                    chunk=response.read(8192)
                    if not chunk: break
                    yield chunk
            finally: response.close()
        return StreamingResponse(chunks(),media_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})
    try:
        result=chat(c['model_path'],messages,c.get('default_model') or 'nexora-local',temperature=body.get('temperature',0.7),max_tokens=body.get('max_tokens',512))
        result['model']=c.get('default_model') or body.get('model','nexora-local'); return result
    except Exception as e: raise HTTPException(503,'Falha no motor/modelo: '+str(e))
@app.post('/v1/completions')
def text_completions(body:dict,authorization:str|None=Header(default=None)):
    auth(authorization)
    if not isinstance(body.get('prompt'),(str,list)): raise HTTPException(400,'Campo prompt obrigatório.')
    response=engine_request('/v1/completions',body)
    if body.get('stream'): return StreamingResponse(response,media_type='text/event-stream')
    from fastapi.responses import Response
    return Response(response.read(),media_type='application/json')
@app.post('/v1/responses')
def responses(body:dict,authorization:str|None=Header(default=None)):
    auth(authorization); response=engine_request('/v1/responses',body)
    from fastapi.responses import Response
    if body.get('stream'): return StreamingResponse(response,media_type='text/event-stream')
    return Response(response.read(),media_type='application/json')
@app.post('/v1/embeddings')
def embeddings(body:dict,authorization:str|None=Header(default=None)):
    auth(authorization); response=engine_request('/v1/embeddings',body)
    from fastapi.responses import Response
    return Response(response.read(),media_type='application/json')


@app.get('/dashboard/tunnel')
def dashboard_tunnel_status(authorization:str|None=Header(default=None)):
    auth(authorization)
    return tunnel_manager.status()

@app.post('/dashboard/tunnel/start')
def dashboard_tunnel_start(authorization:str|None=Header(default=None)):
    auth(authorization)
    c=load()
    if c.get('host') not in ('127.0.0.1','localhost'):
        raise HTTPException(400,'Por segurança, o servidor deve usar 127.0.0.1 antes de compartilhar.')
    try: return tunnel_manager.start(int(c['port']))
    except RuntimeError as e: raise HTTPException(503,str(e))

@app.post('/dashboard/tunnel/stop')
def dashboard_tunnel_stop(authorization:str|None=Header(default=None)):
    auth(authorization)
    return tunnel_manager.stop()
