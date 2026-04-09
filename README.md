<div align="center">

# 🌸 Pétala Hunter

![Status](https://img.shields.io/badge/Status-✅%20Production%20Ready-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-8.1%2B-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Caçador de criativos para Meta Ads Library, Instagram Reels, TikTok e Facebook**  
*Download automático de vídeos em máxima qualidade para análise de campanhas*

[![Demo](screenshots/página_inicial.png)](screenshots/página_download.png)

</div>

## 🚀 Funcionalidades Principais

| Plataforma | Status | Qualidade |
|------------|--------|-----------|
| Meta Ads Library | ✅ Funcionando | 1080p MP4 |
| Instagram Reels | ✅ Funcionando | Full HD |
| TikTok | ✅ Funcionando | Áudio Original |
| Facebook Reels | ✅ Funcionando | Máxima Qualidade |

✅ **Download simultâneo** múltiplos formatos  
✅ **FFmpeg integrado** - Merge vídeo+áudio perfeito  
✅ **Interface intuitiva** - Zero configuração  
✅ **Workflow otimizado** para agências  
✅ **Sem watermark** ou limitação  

## 🎯 Como Usar

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd petala-hunter

# 2. Crie ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac  
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Instale FFmpeg (obrigatório)
# Windows (PowerShell como Admin)
choco install ffmpeg -y
# Linux
sudo apt install ffmpeg
# Mac  
brew install ffmpeg

# 5. Execute
python app.py
```

**Fluxo completo em 30 segundos:**
1. Cole o link da Meta Ads/TikTok/Reel  
2. Clique **"Baixar VídeoReel"**  
3. Receba **MP4 em alta qualidade** ✅

## 📱 Interface
┌─────────────────────────────────────┐
│ Cole URL da Meta Ads Library... │
│ [https://ads...facebook...] │
│ │
│ [📱 Baixar VídeoReel] [📸 FotoReel]│
│ │
│ ✅ Download concluído com sucesso │
│ └─────────────────────────────────┘
│ 📁 Downloads Recentes │
│ - facebook_1635422416581.mp4 🔽 │
│ - tiktok_76102572349.mp4 🔽 │
└─────────────────────────────────────┘

text

## 🛠️ Instalação Completa (Windows)

```powershell
# 1. PowerShell COMO ADMINISTRADOR
choco install ffmpeg -y

# 2. No diretório do projeto
git clone <repo>
cd petala-hunter
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**URL de acesso:** `http://localhost:5000`

## 📦 Dependências

```txt
Flask==3.0.3
yt-dlp==2024.4.9
```

## 🎨 Configurações Avançadas (app.py)

```python
# Qualidade máxima 1080p
"format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]"

# Sem FFmpeg (temporário)
"format": "best[ext=mp4]/best"
```
### Render
Flask app detectado automaticamente

FFmpeg incluído no buildpack

text

## 📈 Resultados Reais
✅ facebook_1635422416581.mp4 [2.1MB - 1080p]
✅ tiktok_76102572349.mp4 [1.8MB - Full HD]
✅ instagram_DWSGTJ8.mp4 [1.4MB - Áudio Original]

text

## 🎨 Identidade Visual - Agência Pétala
🌸 Pétala Hunter™
O criativo certo, na hora certa

Desenvolvido para profissionais de marketing digital

text

![Logo](screenshots/logo.png)

## 📚 Changelog v2.0
✅ [07/04/2026] FFmpeg integrado - merge vídeo+áudio
✅ [07/04/2026] Suporte Meta Ads Library
✅ [07/04/2026] Interface redes sociais completa
✅ [07/04/2026] Download simultâneo Reels/TikTok
✅ [07/04/2026] Nome oficial: Pétala Hunter

text

## 👨‍💼 Sobre o Desenvolvedor

**Pablo Nunes de Oliveira**  
*Analista de Segurança da Informação | SecDevOps*  
💼 **Netsafecorp**  
📚 **Autor:** *Segurança da Informação: Fundamentos Essenciais*  
🎓 **CREA-PA #123456** | **Blue Team | Forense Digital**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)]()
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)]()

## 📞 Suporte Técnico
Para uso comercial ou suporte:
contato@agenciapetala.com.br
WhatsApp: (93)-99106-4376

text

## 📄 Licença
MIT License - © 2026 Agência Pétala
Livre para uso comercial com atribuição

text

---

<div align="center">

**🌸 Pétala Hunter** - *Caçador de criativos para campanhas imbatíveis*  
*Desenvolvido com ❤️ para profissionais de marketing digital*

</div>