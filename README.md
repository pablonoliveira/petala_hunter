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

## Funcionalidades

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

## Início rápido

```powershell
git clone https://github.com/pablonoliveira/petala_hunter.git
cd petala_hunter
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py          # interface web em http://localhost:5000
```

Para baixar vários anúncios de uma vez direto nas pastas dos clientes, veja o [download em lote](docs/download-em-lote.md).

## Estrutura do projeto

```text
petala_hunter/
├── app.py                     # interface web (Flask)
├── baixar_referencias.py      # download em lote (linha de comando)
├── BAIXAR_REFERENCIAS.bat     # atalho para Windows
├── clientes.exemplo.json      # modelo de configuração dos clientes
├── referencias.exemplo.json   # modelo da lista de anúncios
├── requirements.txt
├── templates/ e static/       # front-end
├── docs/                      # documentação detalhada
└── downloads/                 # saída da interface web (fora do git)
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [Instalação e execução](docs/instalacao.md) | Requisitos, instalação no Linux/Windows, dependências e variáveis |
| [Interface web](docs/interface-web.md) | Fluxo de download, nomenclatura dos arquivos e tratamento de erros |
| [Download em lote](docs/download-em-lote.md) | Configuração por cliente, opções, log CSV e limite do Facebook |
| [Limitações e roadmap](docs/limitacoes-e-roadmap.md) | Pontos de atenção e melhorias planejadas |
| [Segurança e deploy](docs/seguranca-e-deploy.md) | Boas práticas antes de publicar e execução com Gunicorn |

> Os criativos baixados pertencem aos respectivos anunciantes. Use-os apenas como referência interna de análise, sem republicar.

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
