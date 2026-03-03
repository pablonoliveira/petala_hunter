```markdown
# 🎯 CreativeHunter – Hunter de Criativos (yt-dlp Web)

**CreativeHunter** é uma aplicação web em **Python + Flask + Socket.IO** para baixar **vídeos e imagens** de Instagram (Reels, Posts, Carrossel), TikTok, **Facebook Ads Library** e +1.000 sites suportados pelo `yt-dlp`.[web:7][web:14]

Focado em **análise de criativos**, benchmarking de concorrentes e estudos de campanhas, com interface alinhada à identidade visual da **Agência Pétala**.

---

## ✨ Funcionalidades

- 📹 **Vídeo/Reel**
  - Instagram Reels, vídeos do feed, Stories públicos
  - TikTok
  - Facebook Ads Library (vídeos de anúncios)
  - Outros sites compatíveis com `yt-dlp`[web:14]

- 🖼 **Foto/Post**
  - Posts de foto do Instagram
  - Carrossel (baixa múltiplas imagens)
  - Thumbnails de vídeos (quando disponíveis)

- 🌐 Interface Web
  - Front-end em Flask + Socket.IO
  - Barra de progresso em tempo real (percentual, velocidade, ETA)
  - Lista de downloads recentes atualizada dinamicamente
  - Visual refinado (Playfair Display + Montserrat, dourado e tons terrosos)

---

## 🗂 Estrutura do Projeto

```bash
CreativeHunter/
├── app.py               # Backend Flask + Socket.IO + yt-dlp
├── requirements.txt     # Dependências Python
├── templates/
│   └── index.html       # Interface CreativeHunter
├── static/
│   └── style.css        # Identidade visual (Agência Pétala)
├── downloads/           # Onde os criativos são salvos
└── README.md
```

---

## 🔧 Requisitos

- Python 3.8+.[cite:3]  
- `ffmpeg` instalado e no PATH (necessário para merge de áudio/vídeo).
- `yt-dlp` (instalado via `pip` com `requirements.txt`).

---

## 🚀 Instalação e Execução

```bash
# 1. Clonar o repositório
git clone https://github.com/pablonoliveira/CreativeHunter.git
cd CreativeHunter

# 2. Criar ambiente virtual (recomendado)
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Garantir pasta de downloads
mkdir downloads

# 5. Rodar aplicação
python app.py
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

---

## 🧠 Como Usar

### 1. Escolher o tipo de conteúdo

Na interface principal:

- **📹 Vídeo/Reel**  
  Para criativos em vídeo:
  - Instagram Reels
  - Vídeos do feed
  - TikTok
  - Facebook Ads Library
  - Outros sites suportados

- **🖼 Foto/Post**  
  Para criativos em imagem:
  - Posts de foto do Instagram
  - Carrossel de imagens (múltiplos arquivos)
  - Thumbnails quando disponíveis

### 2. Exemplos

- **Instagram Reel**
  - URL: `https://www.instagram.com/reel/XXXXXXXXXXX/`
  - Botão: **📹 Vídeo/Reel**
  - Resultado: arquivo `.mp4` em `downloads/`.

- **Instagram Post Foto**
  - URL: `https://www.instagram.com/p/XXXXXXXXXXX/`
  - Botão: **🖼 Foto/Post**
  - Resultado: `.jpg`/`.png` em `downloads/`.

- **Instagram Carrossel**
  - URL: `https://www.instagram.com/p/XXXXXXXXXXX/`
  - Botão: **🖼 Foto/Post**
  - Resultado: vários `.jpg` (um por slide do carrossel).

- **Facebook Ads Library**
  - Abra o anúncio na Biblioteca de Anúncios.[web:23]
  - Clique nos “…” → **Copiar link**.
  - Cole no CreativeHunter → Botão **📹 Vídeo/Reel**.

- **TikTok**
  - URL: `https://www.tiktok.com/@user/video/XXXXXXXXXXX`
  - Botão: **📹 Vídeo/Reel**.

---

## ⚙️ Detalhes Técnicos

### Backend (`app.py`)

- **Flask**: rotas HTTP e renderização de templates.
- **Flask-SocketIO**: envio de eventos de progresso para o front em tempo real.
- **yt-dlp**:
  - Vídeo/Reel:
    ```python
    format='bestvideo[height<=1080]+bestaudio/best'
    ```
  - Foto/Post:
    ```python
    format='image*+bestaudio/bestimage/best'
    ```
  - Configuração para playlists/carrossel:
    ```python
    extract_flat=False
    noplaylist=False
    ```
  - Hook de progresso (`progress_hooks`) atualiza:
    - Porcentagem
    - Velocidade
    - ETA
    - Nome do arquivo

### Frontend (`index.html` + `style.css`)

- Barra de progresso com animação e gradiente dourado.
- Cards de downloads recentes exibindo nome truncado e extensão.
- Responsivo (desktop e mobile).
- Cores e tipografia baseadas no **Manual de Identidade Visual da Agência Pétala**.

---

## 🧪 Troubleshooting

- **Arquivo já existe**  
  - yt-dlp informa 100% imediatamente e não baixa de novo; o arquivo já está em `downloads/`.

- **Erro 429 / verificação / login no Instagram**  
  - O Instagram pode impor rate-limit. Aguarde um tempo ou configure cookies de sessão exportados do navegador e use com yt-dlp (opcional).[web:22]

- **“There is no video in this post”**  
  - Use o botão **🖼 Foto/Post**: é um post de imagem, não vídeo.

---

## 🛡 Aviso Legal

CreativeHunter foi desenvolvido para:
- Estudo de criativos,
- Benchmarking de campanhas,
- Pesquisa e análise em contexto profissional (marketing / segurança / OSINT).

Sempre respeite:
- Termos de uso das plataformas,
- Direitos autorais,
- Legislação aplicável no seu país.

---

## 👨‍💻 Autor

**CreativeHunter** por **Pablo Nunes de Oliveira**  
Analista de Segurança da Informação · Blue Team · OSINT · Agência Pétala  

- GitHub: [@pablonoliveira](https://github.com/pablonoliveira)  
- Local: Itaituba – PA – BR  

> Pull requests, issues e sugestões são bem-vindas!
```