# Download em lote (Meta Ads Library)

Além da interface web, o projeto traz o `baixar_referencias.py`, que baixa uma lista de anúncios da Meta Ads Library de uma vez e salva cada vídeo na pasta do cliente correspondente. É pensado para rotinas de pesquisa de criativos: você monta a lista de referências e o script organiza tudo por cliente e por mês.

## 1. Configurar os clientes

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

## 2. Montar a lista de referências

```bash
copy referencias.exemplo.json referencias.json
```

```json
[
  { "cliente": "Cliente Exemplo", "anunciante": "Anunciante Fictício", "id": "000000000000000" }
]
```

O `id` é a **Identificação da biblioteca** que aparece no anúncio (o número de `facebook.com/ads/library/?id=...`). O valor de `cliente` precisa existir em `clientes.json`.

## 3. Executar

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

## Como o script se comporta

- **Arquivos já baixados são pulados.** Pode rodar de novo quantas vezes precisar: só os que faltam são tentados.
- **Log em CSV.** Ao final é gerado `log_download_<data>.csv` com cliente, anunciante, link, status (`OK`, `JA_EXISTIA`, `ERRO`) e pasta de destino.
- **Limite do Facebook (HTTP 429).** Quando há muitas requisições seguidas, o script espera 60s, 120s e 240s antes de desistir do item. Se ainda sobrarem erros 429, aguarde 20–30 minutos e rode de novo.
- **`Unable to extract ad data`.** Alguns formatos (como carrosséis) não são lidos pelo `yt-dlp`. Baixe esses anúncios manualmente pelo link do log.

## Privacidade dos dados

`clientes.json`, `referencias.json` e `log_download_*.csv` estão no `.gitignore`: a lista de clientes e de pesquisas **nunca** deve ir para o repositório. Versione apenas os arquivos `.exemplo.json`, sempre com dados fictícios.

> Os criativos baixados pertencem aos respectivos anunciantes. Use-os apenas como referência interna de análise, sem republicar.

---

[← Voltar ao README](../README.md)
