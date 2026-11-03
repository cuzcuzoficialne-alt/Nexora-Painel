# NEXORA PAINEL

Painel local de IA com interface escura roxa/amarela, API compatível com OpenAI e gerenciamento de modelos GGUF.

> **Estado:** versão-base inicial (0.1.0). A interface, menu, configuração, download de modelos e rotas HTTP estão implementados. O motor `llama-cpp-python` e o túnel público dependem da compatibilidade/instalação no sistema. Ainda não há garantia de execução em todo Android/Windows/macOS; valide no seu dispositivo antes de anunciar como estável.

## Instalação

Requisitos: Python 3.10+ e Git. Clone o repositório:

```bash
git clone https://github.com/cuzcuzoficialne-alt/Nexora-Painel.git
cd Nexora-Painel
python run.py
```

No Windows PowerShell:

```powershell
git clone https://github.com/cuzcuzoficialne-alt/Nexora-Painel.git
cd Nexora-Painel
py run.py
```

O launcher verifica e instala as dependências Python básicas. No primeiro uso, escolha **Instalar motor de IA**, depois instale um modelo no catálogo. O primeiro download pode ser grande e exige internet e espaço livre.

## API local

Com um modelo instalado e selecionado, escolha **Iniciar IA**. Endpoints:

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

Exemplo:

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer nx-SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"model":"nexora-local","messages":[{"role":"user","content":"Olá!"}]}'
```

A chave gerada fica em `data/config.json` (não compartilhe esse arquivo). A chave também pode ser consultada pelo menu de configurações.

## Roblox / acesso externo

`127.0.0.1` só funciona no próprio aparelho que executa a NEXORA. Para uma experiência Roblox publicada, use um endereço HTTPS público encaminhado para a porta local por um túnel, como Cloudflare Tunnel. O túnel não hospeda o modelo: o processamento continua no dispositivo. Proteja a chave; não a coloque em LocalScripts ou código distribuído aos jogadores. Use um Script do servidor e habilite HTTP Requests nas configurações da experiência.

Esta versão-base ainda não automatiza a instalação/configuração do `cloudflared`; o recurso de túnel será adicionado após validar a execução local em cada plataforma.

## tmux

No Termux/Linux, pode iniciar `tmux` antes de `python run.py`. Fora do tmux, o launcher avisa que fechar a sessão pode interromper o servidor. No Windows/macOS, o menu funciona sem exigir tmux.

## Atualização

Na opção **Atualizar NEXORA**, o programa usa `git pull --ff-only`. Modelos, configuração e backups ficam fora do controle de versão (`models/`, `data/`, `backups/`) e não são removidos pela atualização. Se houver alterações locais conflitantes, a atualização para sem sobrescrever arquivos.

## Limitações conhecidas da base 0.1.0

- `llama-cpp-python` pode precisar de compilação nativa; suporte e instalação variam por sistema, arquitetura e versão do Python. Em Termux, pode exigir ferramentas de compilação e memória adicional.
- RAM indicada no catálogo é uma estimativa aproximada, não uma medição do dispositivo.
- Streaming, completions legadas, múltiplos modelos simultâneos, autenticação multiusuário e túnel automático ainda não estão implementados.
- A API responde em `/v1/chat/completions` e `/v1/models`; o formato específico de uma interface Roblox customizada pode exigir um adaptador.

## Estrutura

```text
Nexora-Painel/
├── run.py
├── nexora/       # CLI, catálogo, motor e API
├── web/          # painel web editável
├── models/       # modelos baixados (não versionados)
├── data/         # configuração e chave (não versionadas)
└── backups/      # backups locais (não versionados)
```

## Segurança

Não exponha a porta local diretamente à internet. Para uso remoto, prefira túnel HTTPS, mantenha a chave secreta, limite quem pode acessá-la e não coloque segredos em código cliente. Esta versão é uma base de desenvolvimento, não um serviço endurecido para produção.

## Licença

Escolha e adicione uma licença antes de publicar o projeto. Verifique também as licenças e termos de cada modelo baixado.
