import os, subprocess, sys, shutil, time, re, threading, webbrowser
from .config import load,save,ROOT
from .catalog import CATALOG
from .models import install,list_installed
def clear():
 os.system('cls' if os.name=='nt' else 'clear')

def goodbye(reason=''):
 print()
 print('╭──────────────────────────────────────────────╮')
 print('│                 NEXORA AI                    │')
 print('│                                              │')
 print('│       ✓ Servidor e recursos finalizados      │')
 print('│       Obrigado por usar a NEXORA!            │')
 print('╰──────────────────────────────────────────────╯')
 if reason: print(reason)
def pause(): input('\nEnter para voltar...')
def install_engine():
 from .engine_setup import install_engine as build_engine
 ok=build_engine()
 print('Motor pronto.' if ok else 'Não foi possível concluir a instalação do motor.')
 pause()

def choose_model():
 print('\nCATÁLOGO NEXORA')
 for i,m in enumerate(CATALOG,1): print(f"[{i}] {m['name']} | {m['class']} | RAM estimada {m['ram']} | {m.get('disk','tamanho varia por quantização')}")
 print('[0] Voltar'); v=input('Número: ').strip()
 if v.isdigit() and 1<=int(v)<=len(CATALOG):
  try: print('Download iniciado...'); print('Salvo em:',install(int(v)-1))
  except Exception as e: print('Erro:',e)
  pause()
def start_tunnel(port):
 from . import tunnel as tunnel_manager
 try:
  result=tunnel_manager.start(port)
  if result.get('url'):
   print('Endereço público:',result['url']); print('API:',result['api_url'])
  else: print('Túnel iniciando. Abra o painel para acompanhar.')
  print('Ctrl+C encerra o túnel com segurança.')
  while tunnel_manager.status().get('running'): time.sleep(1)
 except KeyboardInterrupt:
  print('Finalizando túnel...'); tunnel_manager.stop(); print('✓ Túnel encerrado.')
 except Exception as e: print('Falha no túnel:',e)
 pause()

def start_server():
 cfg=load()
 if not cfg.get('model_path'): print('Instale ou selecione um modelo primeiro.'); pause(); return
 try: import uvicorn; from .server import app
 except Exception as e: print('Dependência/servidor indisponível:',e); pause(); return
 url=f"http://127.0.0.1:{cfg['port']}"
 print('Painel:',url); print('API:',url+'/v1/chat/completions'); print('Servidor iniciado. Pressione Ctrl+C para encerrar.')
 try:
  uvicorn.run(app,host=cfg['host'],port=int(cfg['port']),log_level='warning')
 except KeyboardInterrupt:
  pass
 finally:
  print('\nFinalizando serviços...')
  try:
   from . import tunnel as tunnel_manager
   tunnel_manager.stop()
  except Exception: pass
  try:
   from .engine import stop
   stop()
  except Exception: pass
  print('✓ Serviços finalizados.')
def settings():
 c=load(); print('\n[1] Alterar porta (atual:',c['port'],')\n[2] Mostrar chave\n[3] Gerar nova chave\n[4] Abrir túnel Cloudflare (servidor deve estar iniciado em outra sessão)\n[0] Voltar'); x=input('Escolha: ').strip()
 if x=='1':
  try:
   n=int(input('Porta 1024-65535: ')); assert 1024<=n<=65535; c['port']=n; save(c); print('Porta salva.')
  except Exception: print('Porta inválida.')
 elif x=='2': print(c['api_key'])
 elif x=='3':
  import secrets; c['api_key']='nx-'+secrets.token_urlsafe(30); save(c); print('Nova chave:',c['api_key'])
 elif x=='4': start_tunnel(c['port'])
 pause()
def update():
 print('Verificando atualizações do GitHub...')
 try:
  from .updater import update as safe_update
  result=safe_update()
  print(result['message'])
  if result.get('backup'): print('Backup do código anterior:',result['backup'])
  if result.get('previous'): print('Versão Git:',result['previous'],'→',result['current'])
  if result.get('updated'): print('Reinicie a NEXORA para carregar os arquivos atualizados.')
 except Exception as e:
  print('Atualização cancelada:',e)
 pause()

def menu():
 try:
  _menu_loop()
 except KeyboardInterrupt:
  goodbye('Interrupção pelo teclado (Ctrl+C).')

def _menu_loop():
 while True:
  clear(); c=load(); print('\033[95m========== NEXORA AI 0.9.0 =========\033[0m'); print('Modelo:',c.get('default_model') or 'Nenhum'); print('Modelos baixados:',len(list_installed()))
  print('\n[1] Iniciar painel + API\n[2] Instalar modelo\n[3] Selecionar modelo GGUF instalado\n[4] Listar modelos instalados\n[5] Instalar motor de IA\n[6] Compartilhar API (Cloudflare)\n[7] Configurações / chave\n[8] Atualizar pelo GitHub\n[0] Sair')
  x=input('\nEscolha: ').strip()
  if x=='1': start_server()
  elif x=='2': choose_model()
  elif x=='3':
   fs=list_installed()
   for i,p in enumerate(fs,1): print(f'[{i}] {p.name}')
   v=input('Número: ').strip()
   if v.isdigit() and 1<=int(v)<=len(fs):
    from .models import select_model; select_model(fs[int(v)-1]); print('Modelo padrão alterado.')
   pause()
  elif x=='4':
   for p in list_installed(): print('-',p.name)
   pause()
  elif x=='5': install_engine()
  elif x=='6': start_tunnel(c['port'])
  elif x=='7': settings()
  elif x=='8': update()
  elif x=='0': goodbye(); return
