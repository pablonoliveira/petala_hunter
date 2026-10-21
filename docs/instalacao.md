# Instalação e execução

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
curl_cffi
```

| Pacote | Para quê |
|---|---|
| `Flask` | Interface web |
| `yt-dlp` | Motor de extração. O extrator da Meta Ads Library muda com frequência: se os downloads começarem a falhar, atualize com `pip install -U yt-dlp` |
| `curl_cffi` | Impersonação de navegador, necessária para o **TikTok**. Sem ele, o TikTok responde "Unexpected response from webpage request" |

## Solução de problemas no Windows

- **`Fatal error in launcher: Unable to create process`** ao rodar `pip`: o venv foi copiado de outra pasta e o atalho `pip.exe` aponta para o caminho antigo. Use `python -m pip install ...` ou recrie o venv:

  ```powershell
  deactivate
  Remove-Item -Recurse -Force venv
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  python -m pip install -r requirements.txt
  ```

- **`O termo 'X.bat' não é reconhecido`** no PowerShell: rode com `.\` na frente, ex.: `.\BAIXAR_REFERENCIAS.bat`.
- **Acentos aparecendo como `�`** no terminal: rode `chcp 65001` antes. É só exibição; os arquivos e commits ficam corretos.
- Os atalhos `.bat` usam direto `venv\Scripts\python.exe` (sem depender do `activate.bat`), então funcionam mesmo com o venv copiado de outra pasta.

## Variáveis e execução

O `app.py` considera os seguintes parâmetros de execução:

- `PORT`: define a porta da aplicação; o padrão é `5000`.
- `DEBUG`: habilita modo debug quando definido como `True`.

Exemplo:

```bash
PORT=8000 DEBUG=True python app.py
```

---

[← Voltar ao README](../README.md)
