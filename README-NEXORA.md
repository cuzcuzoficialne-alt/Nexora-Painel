# 💜 NEXORA AI --- Inteligência artificial local

> **Sua IA. Seu dispositivo. Sua API.**
>
> A NEXORA é um projeto open-source para executar modelos de linguagem
> localmente, acessar um painel web e disponibilizar uma API compatível
> com formatos usados por ferramentas de IA.

```{=html}
<p align="center">
```
**Painel local • Modelos GGUF • API • Cloudflare Tunnel**

```{=html}
</p>
```

------------------------------------------------------------------------

## ✨ O que é a NEXORA?

A NEXORA organiza em um só lugar o download de modelos GGUF, o motor
`llama.cpp`, um painel web e uma API local.

-   🧠 **IA local:** o modelo é executado no seu próprio dispositivo.
-   🖥️ **Painel web:** converse com o modelo e gerencie modelos e
    configurações.
-   🔌 **API:** use a IA em outros projetos que aceitam chamadas HTTP.
-   🌐 **Compartilhamento:** Cloudflare Tunnel pode criar um endereço
    HTTPS público temporário.
-   🔐 **Chaves `nx-`:** proteja as chamadas da API.
-   💾 **Seus arquivos:** modelos, configurações e dados ficam nas
    pastas locais ignoradas pelo Git.

> *Atenção:* a velocidade e os modelos disponíveis dependem da memória
> RAM, do processador, do espaço livre e do sistema operacional. Modelos
> maiores não funcionam bem em todos os aparelhos.

## 📋 Antes de começar

Você precisa de:

1.  Python **3.10 ou superior**.
2.  Git.
3.  Internet para baixar o projeto, as dependências, o motor e os
    modelos.
4.  Espaço livre para o modelo escolhido.
5.  Ferramentas de compilação para instalar o `llama.cpp`.

### Android --- Termux

Instale o Termux por uma fonte confiável e abra o aplicativo. Depois
copie e execute:

``` bash
pkg update -y && pkg upgrade -y
pkg install -y git python cmake clang make libandroid-spawn
```

### Linux --- Ubuntu/Debian

Abra o terminal e execute:

``` bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv cmake build-essential
```

Em outras distribuições, instale os equivalentes de Git, Python 3, CMake
e compilador C/C++ usando o gerenciador da sua distribuição.

### Windows

Instale antes:

-   **Python 3.10+** --- marque a opção para adicionar Python ao PATH.
-   **Git for Windows**.
-   **CMake**.
-   **Visual Studio Build Tools**, com a carga de trabalho
    *Desenvolvimento para desktop com C++*.

Depois abra o **PowerShell**.

### macOS

Instale as ferramentas de linha de comando e os utilitários:

``` bash
xcode-select --install
brew install git cmake python
```

> Se algum comando de instalação não existir no seu sistema, procure o
> pacote equivalente para sua distribuição. Não execute comandos de uma
> plataforma em outra.

------------------------------------------------------------------------

## 🚀 Instalação --- passo a passo

### Passo 1 --- Baixar a NEXORA

Abra o terminal e copie o bloco correspondente ao seu sistema.

**Android / Termux / Linux / macOS:**

``` bash
git clone https://github.com/cuzcuzoficialne-alt/Nexora-Painel.git
cd Nexora-Painel
```

**Windows PowerShell:**

``` powershell
git clone https://github.com/cuzcuzoficialne-alt/Nexora-Painel.git
cd Nexora-Painel
```

### Passo 2 --- Iniciar

**Android / Termux / Linux / macOS:**

``` bash
python run.py
```

Se o comando `python` não existir no Linux, tente:

``` bash
python3 run.py
```

**Windows PowerShell:**

``` powershell
py run.py
```

A primeira execução verifica e instala as dependências Python que
estiverem faltando.

### Passo 3 --- Instalar o motor de IA

No menu da NEXORA, escolha:

``` text
[5] Instalar motor de IA
```

A NEXORA baixa o código do `llama.cpp` e tenta compilar o executável
`llama-server`.

-   No Termux, as ferramentas de compilação precisam estar instaladas.
-   No Windows, Git, CMake e Visual Studio Build Tools com C++ precisam
    estar configurados.
-   Em celulares, a compilação pode demorar e consumir bastante memória
    e armazenamento.

Se a compilação falhar, leia a mensagem exibida no terminal e confira se
as ferramentas exigidas estão instaladas.

### Passo 4 --- Baixar um modelo

No menu, escolha:

``` text
[2] Instalar modelo
```

Depois:

1.  Veja o catálogo apresentado.
2.  Confira a classe e a estimativa de RAM/armazenamento.
3.  Digite o número do modelo desejado.
4.  Aguarde o download terminar.

**Dica:** comece por um modelo leve. A estimativa de RAM é aproximada; o
uso real varia com o modelo, a quantização, o contexto e o sistema.

### Passo 5 --- Iniciar o painel

No menu, escolha:

``` text
[1] Iniciar painel + API
```

Quando o servidor iniciar, abra no navegador do mesmo dispositivo:

``` text
http://127.0.0.1:8000
```

Se você alterou a porta nas configurações, use a porta configurada.

> `127.0.0.1` significa "este próprio dispositivo". Um celular,
> computador ou jogo em outro aparelho não consegue acessar o localhost
> do seu dispositivo diretamente.

------------------------------------------------------------------------

## 🧭 Menu da NEXORA

Os números abaixo correspondem ao menu atual:

  Opção   O que faz
  ------- -------------------------------------------------------
  `1`     Inicia painel web e API
  `2`     Abre o catálogo e instala um modelo
  `3`     Seleciona um modelo GGUF já baixado
  `4`     Lista os modelos instalados
  `5`     Instala/compila o motor `llama.cpp`
  `6`     Inicia o compartilhamento Cloudflare Tunnel
  `7`     Abre configurações e gerenciamento da chave principal
  `8`     Procura e aplica atualização do GitHub
  `0`     Sai do menu

*O menu pode mudar em versões futuras.*

## 🌐 Compartilhar a API pela internet

O Cloudflare Tunnel permite criar um endereço HTTPS público que
encaminha requisições para a NEXORA no seu dispositivo.

### Passo 1 --- Instalar o `cloudflared`

Instale o `cloudflared` seguindo as instruções oficiais para o seu
sistema:

<https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/>

Confirme que o comando está disponível:

``` bash
cloudflared --version
```

### Passo 2 --- Iniciar o servidor

Em um terminal, abra a pasta da NEXORA e execute:

``` bash
python run.py
```

No menu, escolha `1` para iniciar o painel e a API. Deixe esse terminal
aberto.

### Passo 3 --- Iniciar o túnel

Abra **outro terminal**, entre novamente na pasta do projeto e execute:

``` bash
python run.py
```

No segundo menu, escolha:

``` text
[6] Compartilhar API (Cloudflare)
```

Aguarde a URL `https://....trycloudflare.com`.

O túnel precisa permanecer ativo para o endereço funcionar. O endereço
Quick Tunnel é temporário e pode mudar quando o túnel for reiniciado.

> **Importante:** se o aparelho desligar, perder a internet ou o
> processo for encerrado, a API deixa de responder. O processamento
> continua sendo feito no seu próprio dispositivo; o túnel não hospeda
> nem acelera o modelo.

## 🔑 Chave da API

A NEXORA usa chaves no formato `nx-...`.

-   A chave principal é criada na configuração local.
-   Chaves adicionais podem ser gerenciadas na área de chaves do painel.
-   Envie a chave no cabeçalho HTTP `Authorization`.
-   Não publique sua chave em repositórios, prints, vídeos ou mensagens
    públicas.
-   Não coloque a chave em um `LocalScript` do Roblox ou em código
    executado no navegador.

**Exemplo de cabeçalho:**

``` http
Authorization: Bearer nx-SUA_CHAVE_AQUI
```

Substitua `nx-SUA_CHAVE_AQUI` pela sua chave real. Não use esse texto de
exemplo como chave.

## 🔌 Usar a API

Com o servidor ligado, a API local fica normalmente em:

``` text
http://127.0.0.1:8000
```

### Verificar se está online

``` bash
curl http://127.0.0.1:8000/health
```

### Listar modelos

``` bash
curl http://127.0.0.1:8000/v1/models \
  -H "Authorization: Bearer nx-SUA_CHAVE_AQUI"
```

### Enviar uma conversa

``` bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer nx-SUA_CHAVE_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nexora-local",
    "messages": [
      {"role": "user", "content": "Oi! Explique em uma frase o que você consegue fazer."}
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

No Windows PowerShell, `curl` pode ser um alias. Se o exemplo acima não
funcionar, use `curl.exe` no lugar de `curl`.

### Endpoints disponíveis

  Método     Rota                         Uso
  ---------- ---------------------------- ---------------------------
  `GET`      `/health`                    Estado básico do serviço
  `GET`      `/v1/models`                 Lista modelos pela API
  `POST`     `/v1/chat/completions`       Conversa em formato chat
  `POST`     `/v1/completions`            Formato de completions
  `POST`     `/v1/responses`              Formato responses
  `POST`     `/v1/embeddings`             Rota de embeddings
  `GET`      `/dashboard/status`          Estado do painel
  `GET`      `/dashboard/models`          Modelos locais instalados
  `GET`      `/dashboard/keys`            Gerenciamento de chaves
  `POST`     `/dashboard/keys`            Criar chave
  `DELETE`   `/dashboard/keys/{key_id}`   Revogar chave
  `POST`     `/dashboard/tunnel/start`    Iniciar túnel
  `POST`     `/dashboard/tunnel/stop`     Encerrar túnel

*Compatibilidade e parâmetros variam conforme o motor e o modelo. Nem
todos os recursos avançados da API OpenAI são garantidos. A rota de
embeddings depende de suporte apropriado do motor/modelo.*

------------------------------------------------------------------------

## 🎮 Usar com Roblox

**Atenção:** as requisições HTTP devem sair de um `Script` do servidor
da experiência, nunca de um `LocalScript` com a chave secreta.

### Passo 1 --- Preparar o Roblox Studio

1.  Abra sua experiência no Roblox Studio.
2.  Entre em **Game Settings → Security**.
3.  Ative **Allow HTTP Requests**.
4.  Adicione um `Script` dentro de `ServerScriptService`.

### Passo 2 --- Colocar o código

Troque `SUA_URL_PUBLICA` pela URL HTTPS do seu túnel e `SUA_CHAVE_NX`
pela sua chave real.

``` lua
local HttpService = game:GetService("HttpService")

local API_URL = "SUA_URL_PUBLICA/v1/chat/completions"
local API_KEY = "SUA_CHAVE_NX"

local function perguntarNexora(pergunta)
    local body = {
        model = "nexora-local",
        messages = {
            {
                role = "user",
                content = pergunta
            }
        },
        max_tokens = 150,
        temperature = 0.7
    }

    local sucesso, resposta = pcall(function()
        return HttpService:RequestAsync({
            Url = API_URL,
            Method = "POST",
            Headers = {
                ["Content-Type"] = "application/json",
                ["Authorization"] = "Bearer " .. API_KEY
            },
            Body = HttpService:JSONEncode(body)
        })
    end)

    if not sucesso then
        warn("Erro ao conectar com a NEXORA:", resposta)
        return nil
    end

    if not resposta.Success then
        warn("A API respondeu com erro:", resposta.StatusCode, resposta.Body)
        return nil
    end

    local dados = HttpService:JSONDecode(resposta.Body)
    local escolha = dados.choices and dados.choices[1]

    if escolha and escolha.message then
        return escolha.message.content
    end

    return nil
end

local resposta = perguntarNexora("Olá! Diga oi aos jogadores.")
if resposta then
    print("NEXORA:", resposta)
end
```

> **Segurança:** scripts do servidor não devem entregar a chave ao
> cliente. Para jogos públicos, considere também limites de uso,
> validação de entrada e proteção contra spam. Nunca permita que o
> jogador escolha livremente qualquer URL para o servidor acessar.

### Passo 3 --- Testar

1.  Deixe a NEXORA ligada no dispositivo.
2.  Deixe o Cloudflare Tunnel ativo.
3.  Confirme que a URL pública abre e que a API está respondendo.
4.  Inicie um teste no Roblox Studio.
5.  Confira a janela **Output** para ver a resposta ou o erro.

*O exemplo é um ponto de partida. A integração precisa ser testada no
seu jogo e na sua rede; não há garantia de disponibilidade contínua do
Quick Tunnel.*

------------------------------------------------------------------------

## 💾 Onde ficam seus arquivos?

  Pasta/arquivo             Conteúdo
  ------------------------- ----------------------------------------
  `models/`                 Modelos GGUF baixados
  `data/config.json`        Porta, modelo padrão e chave principal
  `data/api_keys.json`      Chaves adicionais da API
  `data/llama-server.log`   Log do motor, quando gerado
  `backups/`                Backups do atualizador
  `.nexora-runtime/`        Código e compilação do `llama.cpp`

**Não compartilhe `data/` nem publique suas chaves.** Essas pastas são
ignoradas pelo Git para evitar enviar dados pessoais e arquivos grandes
ao repositório.

## 🔄 Atualizar a NEXORA

Se você instalou usando `git clone`, abra a pasta do projeto e execute:

``` bash
python run.py
```

No menu, escolha:

``` text
[8] Atualizar pelo GitHub
```

O atualizador cria um backup dos arquivos versionados e tenta aplicar
somente uma atualização Fast-forward. Se detectar alterações locais em
arquivos versionados, cancela a operação para evitar sobrescrever seu
trabalho.

> Os backups de atualização guardam o código versionado anterior. Eles
> não são uma cópia completa dos modelos ou dos dados locais. Faça
> também suas próprias cópias de segurança importantes.

Depois de atualizar, feche e inicie a NEXORA novamente.

## 🛑 Encerrar corretamente

No terminal em que o servidor está rodando, pressione:

``` text
Ctrl + C
```

A NEXORA tenta encerrar o servidor, o motor e o túnel e mostra uma
mensagem de despedida.

Se estiver usando `tmux`:

-   `Ctrl + B`, depois `D`: destaca a sessão sem encerrar o processo.
-   Para encerrar o servidor, volte à sessão e use `Ctrl + C`.

Fora do `tmux`, mantenha o terminal aberto enquanto estiver usando a
NEXORA. Fechar o terminal pode interromper o serviço.

## 🧰 Problemas comuns

### `python: command not found`

Tente:

``` bash
python3 run.py
```

No Windows, tente:

``` powershell
py run.py
```

### `llama-server não encontrado`

Abra o menu e escolha:

``` text
[5] Instalar motor de IA
```

Se falhar, confira Git, CMake e compilador C/C++.

### Falta de memória ou modelo não carrega

-   Feche aplicativos que não está usando.
-   Tente um modelo menor.
-   Reduza o contexto nas configurações.
-   Confira o espaço livre no dispositivo.
-   Consulte `data/llama-server.log`.

### A API responde `401`

Confira se você enviou:

``` http
Authorization: Bearer nx-SUA_CHAVE_AQUI
```

Confirme também se a chave não foi revogada e se não há espaços extras.

### O endereço público não funciona

-   Confirme que o servidor local está ligado.
-   Confirme que `cloudflared` está instalado.
-   Confira se o processo do túnel continua ativo.
-   Gere outro Quick Tunnel se o endereço anterior expirou ou mudou.

### O Roblox não consegue conectar

-   Ative **Allow HTTP Requests**.
-   Use a URL HTTPS pública do túnel, não `127.0.0.1`.
-   Confira a chave.
-   Faça a requisição em um `Script` do servidor.
-   Veja os erros no Output do Studio e nos logs da NEXORA.

------------------------------------------------------------------------

## 🔐 Segurança e uso responsável

-   Proteja suas chaves `nx-`.
-   Não exponha a chave em scripts de cliente, páginas públicas ou
    repositórios.
-   Compartilhe a URL pública somente com quem deve acessar.
-   O túnel público permite que outras pessoas alcancem seu serviço;
    mantenha a autenticação ativa.
-   Não use a API para spam, abuso ou atividades ilegais.
-   Revogue imediatamente uma chave que tenha sido exposta.

## 🧪 Estado do projeto

A NEXORA está em desenvolvimento. A compilação e os testes locais de
rotas não significam que todas as combinações de sistema, modelo,
dispositivo, Cloudflare ou Roblox foram testadas.

O funcionamento real depende do ambiente e dos recursos do aparelho.
Relate erros com a mensagem completa do terminal, removendo antes
qualquer chave ou informação privada.

## 📦 Repositório

**GitHub:** <https://github.com/cuzcuzoficialne-alt/Nexora-Painel>

Se este projeto ajudar você, considere deixar uma ⭐ no repositório e
compartilhar melhorias.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
**💜 NEXORA AI --- Sua inteligência, do seu jeito. 💛**

*Feito para experimentar, aprender e construir.*

```{=html}
</p>
```
