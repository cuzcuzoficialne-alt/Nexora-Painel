from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download
from .catalog import CATALOG
from .config import MODELS, load, save
def list_installed(): return sorted(p for p in MODELS.glob('*.gguf') if p.is_file())
def choose_file(repo):
    files=HfApi().list_repo_files(repo); ggufs=[f for f in files if f.lower().endswith('.gguf')]
    if not ggufs: raise RuntimeError('Nenhum arquivo GGUF encontrado neste repositório.')
    ranked=sorted(ggufs,key=lambda f:(0 if 'Q4_K_M' in f.upper() else 1 if 'Q4' in f.upper() else 2, len(f)))
    return ranked[0]
def install(index):
    item=CATALOG[index]; print(f"Consultando {item['repo']}...")
    filename=choose_file(item['repo']); print('Arquivo:',filename)
    path=hf_hub_download(repo_id=item['repo'],filename=filename,local_dir=str(MODELS))
    cfg=load(); cfg.update(default_model=item['id'],model_path=str(Path(path).resolve())); save(cfg); return path
def select_model(path):
    p=Path(path).resolve()
    if not p.is_file() or p.suffix.lower()!='.gguf': raise ValueError('Arquivo GGUF inválido.')
    cfg=load(); cfg.update(model_path=str(p),default_model=p.stem); save(cfg)
