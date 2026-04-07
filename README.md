```markdown

# ** 🎯 CreativeHunter – Hunter de Criativos (yt-dlp Web)**

[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)](https://creativehunter-production.up.railway.app)
[![GitHub](https://img.shields.io/badge/GitHub-CreativeHunter-blue?style=flat-square&logo=github)](https://github.com/pablonoliveira/CreativeHunter)
[![Live](https://img.shields.io/badge/Live-Railway-0B0D17?style=flat-square&logo=railway)](https://creativehunter-production.up.railway.app)
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://python.org)  
[![Flask](https://img.shields.io/badge/flask-3.0%2B-red.svg)](https://flask.palletsprojects.com/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**CreativeHunter** é uma aplicação web em **Python + Flask + Socket.IO** para baixar **vídeos e imagens** de Instagram (Reels, Posts, Carrossel), TikTok, **Facebook Ads Library** e +1.000 sites suportados pelo `yt-dlp`.

Focado em **análise de criativos**, benchmarking de concorrentes e estudos de campanhas, com interface alinhada à identidade visual da **Agência Pétala**.

---

## 🚀 Quick Start

```bash
# Clone o repositório
git clone https://github.com/pablonoliveira/CreativeHunter.git
cd CreativeHunter

# Crie e ative venv
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Instale dependências
pip install -r requirements.txt

# Rode localmente
python app.py
```

Acesse: **http://localhost:5000**

---
## ✨ Funcionalidades

### 📹 Vídeo/Reel
- Instagram Reels, vídeos do feed, Stories públicos
- TikTok
- Facebook Ads Library (vídeos de anúncios)
- Outros sites compatíveis com `yt-dlp`

### 🖼 Foto/Post
- Posts de foto do Instagram
- Carrossel (baixa múltiplas imagens)
- Thumbnails de vídeos (quando disponíveis)

### 🌐 Interface Web
- Front-end em Flask + Socket.IO
- Barra de progresso em tempo real (percentual, velocidade, ETA)
- Lista de downloads recentes atualizada dinamicamente
- Visual refinado (Playfair Display + Montserrat, dourado e tons terrosos)

---

## 📊 Screenshots

### Interface Principal
```
CreativeHunter
Hunter de criativos: Instagram Reels/Posts -  TikTok -  Facebook Ads -  +1.000 sites

[URL Input] [📹 Vídeo/Reel] [🖼️ Foto/Post]

Barra de progresso | 45% | 1.2MiB/s | ETA 00:05
```

---

## 🗂 Estrutura do Projeto

```bash
CreativeHunter/
├── app.py                   # Backend Flask + Socket.IO + yt-dlp
├── requirements.txt         # Dependências Python
├── Dockerfile              # Docker (opcional)
├── .gitignore              # Git ignore
├── LICENSE                 # MIT License
├── README.md               # Este arquivo
├── templates/
│   └── index.html          # Interface CreativeHunter
├── static/
│   └── style.css           # Identidade visual (Agência Pétala)
├── downloads/              # Onde os criativos são salvos (local)
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions (optional)
```

---

## 🔧 Requisitos

- **Python 3.8+**
- **ffmpeg** instalado e no PATH (necessário para merge de áudio/vídeo)
- **yt-dlp** (instalado via `pip`)

### Verificar instalação:
```bash
python --version
ffmpeg -version
```

---

## 📦 Instalação Detalhada

### 1. Clonar repositório
```bash
git clone https://github.com/pablonoliveira/CreativeHunter.git
cd CreativeHunter
```

### 2. Ambiente virtual
```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Criar pasta downloads
```bash
mkdir downloads
```

### 5. Rodar aplicação
```bash
python app.py
```

Acesse: **http://127.0.0.1:5000**

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

#### Instagram Reel
```
URL: https://www.instagram.com/reel/XXXXXXXXXXX/
Botão: 📹 Vídeo/Reel
Resultado: arquivo .mp4 em downloads/
```

#### Instagram Post Foto
```
URL: https://www.instagram.com/p/XXXXXXXXXXX/
Botão: 🖼 Foto/Post
Resultado: .jpg/.png em downloads/
```

#### Instagram Carrossel
```
URL: https://www.instagram.com/p/XXXXXXXXXXX/
Botão: 🖼 Foto/Post
Resultado: vários .jpg (um por slide do carrossel)
```

#### Facebook Ads Library
```
1. Abra o anúncio na Biblioteca de Anúncios
2. Clique nos "…" → "Copiar link"
3. Cole no CreativeHunter → 📹 Vídeo/Reel
```

#### TikTok
```
URL: https://www.tiktok.com/@user/video/XXXXXXXXXXX
Botão: 📹 Vídeo/Reel
```

---

## ⚙️ Detalhes Técnicos

### Backend (`app.py`)

- **Flask**: Rotas HTTP e renderização de templates
- **Flask-SocketIO**: Envio de eventos de progresso em tempo real
- **yt-dlp**: Download de mídias com suporte a +1.000 sites
  - Vídeo/Reel: `format='bestvideo[height<=1080]+bestaudio/best'`
  - Foto/Post: `format='image*+bestaudio/bestimage/best'`
  - Suporta playlists/carrossel automaticamente

### Frontend (`index.html` + `style.css`)

- Barra de progresso com animação e gradiente dourado
- Cards de downloads recentes
- Responsivo (desktop e mobile)
- Tipografia: **Playfair Display** (títulos) + **Montserrat** (texto)
- Cores: **Dourado** `#B89B79`, **Preto** `#0A0B0B`, **Branco** `#FCFCFB`

---

## 🚀 Deploy na Nuvem (Railway)

CreativeHunter está deployado automaticamente no **Railway**!

### Para fazer seu próprio deploy:

1. Crie conta em [railway.com](https://railway.com)
2. Conecte seu repositório GitHub
3. Railway detecta `requirements.txt` e faz deploy automático
4. Toda vez que você faz `git push`, Railway redeploy

**Variáveis de ambiente** (opcional):
```
DEBUG=False
PORT=8080
```

---

## 🧪 Troubleshooting

### Arquivo já existe
- yt-dlp informa 100% imediatamente; arquivo já está em `downloads/`

### Erro 429 / verificação / login no Instagram
- Instagram pode impor rate-limit
- Aguarde um tempo ou configure cookies de sessão

### "There is no video in this post"
- Use botão **🖼 Foto/Post**: é um post de imagem, não vídeo

---

## 🛡 Aviso Legal

CreativeHunter foi desenvolvido para:
- Estudo de criativos
- Benchmarking de campanhas
- Pesquisa e análise em contexto profissional

Sempre respeite:
- Termos de uso das plataformas
- Direitos autorais
- Legislação aplicável no seu país

---

## 🤝 Contribuindo

Pull requests são bem-vindas! Para mudanças maiores, abra uma issue primeiro.

```bash
# Fluxo de contribuição
git checkout -b feature/nova-funcao
git commit -m "feat: adicionar nova funcionalidade"
git push origin feature/nova-funcao
# Abra um Pull Request no GitHub
```

---

## 📝 Roadmap

- [ ] Seleção de qualidade de vídeo
- [ ] Fila de downloads
- [ ] Autenticação multiusuário
- [ ] Export de metadados (JSON/CSV)
- [ ] Dashboard com estatísticas
- [ ] Integração com WhatsApp/Telegram

---

## 👨‍💻 Autor

**CreativeHunter** por **Pablo Nunes de Oliveira**

- Analista de Segurança da Informação
- Blue Team | OSINT | SecDevOps
- Agência Pétala
- 🌍 Itaituba – PA – BR

**Links:**
- GitHub: [@pablonoliveira](https://github.com/pablonoliveira)
- Instagram: [@agencia.petala](https://instagram.com/agencia.petala)

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para detalhes.

---

> **Criado com ❤️ para marketers, analistas de segurança e hunters de criativos.**
>
> Se CreativeHunter foi útil, dê uma ⭐ no GitHub!
```
