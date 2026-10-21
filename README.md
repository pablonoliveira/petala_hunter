<div align="center">

# 🌸 Pétala Hunter

**Caçador de criativos para Meta Ads Library, Instagram Reels, TikTok e Facebook**  
Download automático de mídias para análise de campanhas, com interface web simples, renomeação inteligente e organização local dos arquivos.

![Status](https://img.shields.io/badge/status-em%20evolu%C3%A7%C3%A3o-b89b79)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![Flask](https://img.shields.io/badge/flask-3.x-000000)
![yt--dlp](https://img.shields.io/badge/yt--dlp-suportado-ff4b4b)
![License](https://img.shields.io/badge/license-MIT-yellow)

</div>

## Visão geral

O **Pétala Hunter** é uma aplicação Flask voltada à captura de criativos a partir de URLs públicas de plataformas como Meta Ads Library, Instagram Reels, TikTok e Facebook. O fluxo atual permite colar um link, escolher o tipo de mídia e baixar o arquivo diretamente pela interface, salvando o resultado na pasta `downloads/` com nomes padronizados e mais limpos.

O projeto usa **Flask** para a interface web e **yt-dlp** como motor de extração. Quando necessário, os arquivos baixados passam por um processo de renomeação inteligente para facilitar organização, especialmente em casos com múltiplos itens no mesmo conteúdo.

## Funcionalidades atuais

- Download de mídia por URL pública.
- Suporte a dois modos de captura: **vídeo** e **imagem**.
- Integração com `yt-dlp` para extração dos conteúdos suportados.
- Renomeação automática dos arquivos após o download.
- Lista dos downloads mais recentes na interface.
- Mensagens de erro tratadas para cenários comuns.
- Estrutura simples para execução local ou deploy leve.
- **Download em lote** de criativos da Meta Ads Library direto para as pastas de cada cliente (ex.: Google Drive para Desktop), com log em CSV.

## Plataformas contempladas

As plataformas abaixo aparecem no posicionamento atual do projeto e no fluxo descrito da aplicação:

| Plataforma | Objetivo no projeto | Observação |
|---|---|---|
| Meta Ads Library | Captura de criativos públicos | Sujeito às capacidades e mudanças do `yt-dlp` |
| Instagram Reels | Download de mídia pública | Pode depender de disponibilidade pública do conteúdo |
| TikTok | Download de mídia pública | Pode variar conforme URL e restrições do post |
| Facebook | Download de mídia pública | Alguns conteúdos podem exigir autenticação |

> **Importante:** a compatibilidade real depende da disponibilidade pública da URL, de mudanças nas plataformas e da versão do `yt-dlp` instalada.

## Estrutura do projeto

```text
petala_hunter/
├── app.py
├── baixar_referencias.py        # download em lote (linha de comando)
├── BAIXAR_REFERENCIAS.bat        # atalho para Windows
├── clientes.exemplo.json         # modelo de configuração dos clientes
├── referencias.exemplo.json      # modelo da lista de anúncios
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── downloads/
└── README.md
```

> A estrutura acima representa a organização esperada a partir dos arquivos identificados no projeto. Os nomes de pastas podem variar ligeiramente conforme a versão do repositório.

## Como funciona

1. O usuário cola uma URL pública no formulário.
2. Escolhe o modo de download: `video` ou `imagem`.
3. A aplicação monta as opções do `yt-dlp` conforme o tipo selecionado.
4. O conteúdo é baixado para a pasta `downloads/`.
5. Os arquivos recém-gerados são identificados e renomeados com base no extrator e no ID da mídia.
6. A interface exibe a mensagem de resultado e a lista de arquivos recentes.

## Requisitos

- Python 3.9 ou superior
- `pip`
- Ambiente virtual recomendado
- FFmpeg opcional, mas recomendado para fluxos multimídia mais robustos

## Instalação

### Linux / macOS

```bash
git clone https://github.com/pablonoliveira/petala_hunter.git
cd petala_hunter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/pablonoliveira/petala_hunter.git
cd petala_hunter
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Acesso local

Após iniciar a aplicação, acesse no navegador:

```text
http://localhost:5000
```

A porta também pode ser alterada pela variável de ambiente `PORT`.

## Dependências principais

O núcleo atual do projeto é baseado em:

```txt
Flask>=3.0.3
yt-dlp>=2026.08.19
```

> O extrator da Meta Ads Library muda com frequência. Se os downloads começarem a falhar, atualize com `pip install -U yt-dlp`.

## Variáveis e execução

O `app.py` considera os seguintes parâmetros de execução:

- `PORT`: define a porta da aplicação; o padrão é `5000`.
- `DEBUG`: habilita modo debug quando definido como `True`.

Exemplo:

```bash
PORT=8000 DEBUG=True python app.py
```

## Organização dos downloads

Os arquivos são salvos na pasta `downloads/` e passam por normalização de nome. O padrão usa o extrator e o identificador da mídia como base, o que ajuda a evitar nomes longos, caracteres inválidos e colisões simples entre arquivos.

Exemplos de nomenclatura:

```text
facebook_123456789.mp4
instagram_ABCDEF123.jpg
tiktok_987654321_1.jpg
```

## Tratamento de erros

A aplicação já trata alguns cenários comuns com mensagens mais amigáveis, por exemplo:

- URL não suportada
- Conteúdo privado ou com autenticação
- Post sem vídeo no modo selecionado
- Falha de extração na Meta Ads Library
- Nome de arquivo excessivamente longo

## Download em lote (Meta Ads Library)

Além da interface web, o projeto traz o `baixar_referencias.py`, que baixa uma lista de anúncios da Meta Ads Library de uma vez e salva cada vídeo na pasta do cliente correspondente. É pensado para rotinas de pesquisa de criativos: você monta a lista de referências e o script organiza tudo por cliente e por mês.

### 1. Configurar os clientes

Copie o modelo e ajuste para o seu ambiente:

```bash
copy clientes.exemplo.json clientes.json
```

```json
{
  "raiz": "G:\\Meu Drive\\MINHA AGENCIA",
  "clientes": {
    "Cliente Exemplo": {
      "pasta": "01-CLIENTE EXEMPLO",
      "subpasta": "Pesquisa de Anúncios"
    },
    "Cliente Exemplo - Campanha B": {
      "pasta": "01-CLIENTE EXEMPLO",
      "subpasta": "Pesquisa de Anúncios",
      "prefixo": "CampanhaB_"
    }
  }
}
```

| Campo | Descrição |
|---|---|
| `raiz` | Pasta base onde ficam as pastas dos clientes. Com o Google Drive para Desktop, os arquivos sobem para o Drive automaticamente. |
| `pasta` | Pasta do cliente, relativa à raiz (aceita subpastas, ex.: `GRUPO\CLIENTE`). |
| `subpasta` | Onde os vídeos serão salvos dentro da pasta do cliente. Padrão: `Pesquisa de Anúncios`. |
| `prefixo` | Opcional. Texto no início do nome do arquivo, útil para separar campanhas de um mesmo cliente. |

### 2. Montar a lista de referências

```bash
copy referencias.exemplo.json referencias.json
```

```json
[
  { "cliente": "Cliente Exemplo", "anunciante": "Anunciante Fictício", "id": "000000000000000" }
]
```

O `id` é a **Identificação da biblioteca** que aparece no anúncio (o número de `facebook.com/ads/library/?id=...`). O valor de `cliente` precisa existir em `clientes.json`.

### 3. Executar

No Windows, dê dois cliques em `BAIXAR_REFERENCIAS.bat` ou rode no terminal:

```powershell
.\BAIXAR_REFERENCIAS.bat              # baixa toda a lista
.\BAIXAR_REFERENCIAS.bat --teste 3    # baixa só os 3 primeiros
```

Ou diretamente com Python (venv ativo):

```bash
python baixar_referencias.py --mes NOVEMBRO --pausa 8
```

| Opção | Padrão | Descrição |
|---|---|---|
| `--clientes` | `clientes.json` | Arquivo de configuração dos clientes |
| `--referencias` | `referencias.json` | Lista de anúncios a baixar |
| `--raiz` | valor de `clientes.json` | Sobrescreve a pasta raiz |
| `--mes` | mês atual | Nome da subpasta do mês (`OUTUBRO`, `NOVEMBRO`…) |
| `--teste N` | — | Baixa apenas os N primeiros itens |
| `--pausa` | `6` | Segundos de espera entre downloads |

Cada vídeo é salvo como:

```text
<raiz>\<pasta>\<subpasta>\<MÊS>\<prefixo><Anunciante>_<ID>.mp4
```

### Como o script se comporta

- **Arquivos já baixados são pulados.** Pode rodar de novo quantas vezes precisar: só os que faltam são tentados.
- **Log em CSV.** Ao final é gerado `log_download_<data>.csv` com cliente, anunciante, link, status (`OK`, `JA_EXISTIA`, `ERRO`) e pasta de destino.
- **Limite do Facebook (HTTP 429).** Quando há muitas requisições seguidas, o script espera 60s, 120s e 240s antes de desistir do item. Se ainda sobrarem erros 429, aguarde 20–30 minutos e rode de novo.
- **`Unable to extract ad data`.** Alguns formatos (como carrosséis) não são lidos pelo `yt-dlp`. Baixe esses anúncios manualmente pelo link do log.

### Privacidade dos dados

`clientes.json`, `referencias.json` e `log_download_*.csv` estão no `.gitignore`: a lista de clientes e de pesquisas **nunca** deve ir para o repositório. Versione apenas os arquivos `.exemplo.json`, sempre com dados fictícios.

> Os criativos baixados pertencem aos respectivos anunciantes. Use-os apenas como referência interna de análise, sem republicar.

## Limitações atuais

Este projeto depende diretamente do comportamento do `yt-dlp` e da acessibilidade pública das URLs. Isso significa que mudanças nas plataformas podem impactar o funcionamento sem aviso prévio.

Pontos importantes:

- Nem toda URL pública continuará funcionando ao longo do tempo.
- Conteúdos privados, restritos ou protegidos por login podem falhar.
- Plataformas mudam seletores, endpoints e políticas com frequência.
- O suporte a carrosséis, imagens e vídeos pode variar por plataforma.

## Melhorias recomendadas

Para a próxima versão, estas evoluções tendem a gerar mais estabilidade e manutenibilidade:

- Separar a lógica de download da camada Flask.
- Criar serviços por plataforma.
- Mover configurações para variáveis de ambiente.
- Remover segredo fixo do código-fonte.
- Adicionar logs estruturados.
- Criar testes unitários para normalização, renomeação e tratamento de erros.
- Versionar melhor as capacidades por plataforma.
- Adicionar fila assíncrona para downloads mais pesados.

## Segurança

Antes de publicar uma nova versão, é recomendável:

- substituir a `SECRET_KEY` fixa por variável de ambiente;
- validar tamanho e formato das URLs recebidas;
- limitar concorrência e volume de downloads;
- revisar exposição pública da pasta `downloads`;
- registrar falhas sem vazar detalhes sensíveis ao usuário final.

## Deploy

Por ser um projeto Flask enxuto, o Pétala Hunter pode ser executado localmente, em VPS, contêiner Docker ou plataformas de deploy compatíveis com Python. Em ambientes de produção, é recomendável usar um servidor WSGI como Gunicorn e persistência adequada para a pasta de downloads.

Exemplo com Gunicorn:

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## Licença

Este projeto está licenciado sob os termos da **MIT License**.

## Autor

**Pablo Nunes de Oliveira**  
Analista de Segurança da Informação | Blue Team | Forense Digital | Resposta a Incidentes

GitHub: https://github.com/pablonoliveira

---

<div align="center">
Feito para acelerar a análise de criativos e simplificar o fluxo de captura de mídia.
</div>
