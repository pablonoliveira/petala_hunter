"""
Pétala Hunter - Captador de Criativos para Meta Ads, Reels e TikTok
Download automático em máxima qualidade.

Versão PROD: Flask + yt-dlp com nomes curtos e sanitizados para Railway
Corrige definitivamente o erro 'File name too long' em fotos/posts do Facebook.
"""
from flask import Flask, request, render_template, send_from_directory
import os
import re
import yt_dlp
from pathlib import Path


app = Flask(__name__)
app.config["SECRET_KEY"] = "petala-hunter-2026"

PASTA_DOWNLOADS = "downloads"
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)


def listar_arquivos():
    """Lista os 12 arquivos mais recentes da pasta downloads."""
    if not os.path.exists(PASTA_DOWNLOADS):
        return []

    arquivos = [
        f for f in os.listdir(PASTA_DOWNLOADS)
        if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
    ]
    return sorted(arquivos, reverse=True)[:12]


def sanitizar_mensagem_erro(erro):
    """Converte erros técnicos em mensagens amigáveis para o usuário."""
    msg = str(erro)

    if "There is no video in this post" in msg:
        return "❌ Esse post não possui vídeo disponível para o modo selecionado."

    if "facebook:ads" in msg and "Unable to extract ad data" in msg:
        return "❌ Esse criativo da Meta Ads Library não pôde ser extraído pela versão atual do yt-dlp."

    if "Unsupported URL" in msg:
        return "❌ Essa URL não é suportada pelo Pétala Hunter."

    if "Private video" in msg or "login required" in msg.lower():
        return "❌ O conteúdo exige autenticação ou não está acessível publicamente."

    if "File name too long" in msg:
        return "❌ Nome do arquivo muito longo. Correção aplicada no salvamento."

    return f"❌ Erro ao processar o link: {msg[:160]}"


def limpar_nome_arquivo(texto):
    """Remove caracteres inválidos e limita tamanho do nome do arquivo."""
    texto = texto or "arquivo"
    texto = re.sub(r'[\\/*?:"<>|=&]', "", texto)
    texto = re.sub(r"\s+", "_", texto).strip("_")
    return texto[:80]


def montar_opcoes_ydl(tipo):
    """
    Configura opções do yt-dlp.
    Mantém nome temporário curto e depois renomeia no pós-download.
    """
    nome_saida = os.path.join(PASTA_DOWNLOADS, "%(extractor)s_%(id)s.%(ext)s")

    opcoes_base = {
        "outtmpl": nome_saida,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": False,
        "extract_flat": False,
        "windowsfilenames": True,
        "restrictfilenames": True,
        "trim_file_name": 80,
    }

    if tipo == "imagem":
        opcoes_base.update({
            "format": "best[ext=jpg]/best[ext=jpeg]/best[ext=png]/best"
        })
    else:
        opcoes_base.update({
            "format": "best[ext=mp4]/best"
        })

    return opcoes_base


def encontrar_arquivo_recente(antes, depois):
    """Identifica o arquivo novo criado após o download."""
    novos = list(depois - antes)
    if novos:
        caminhos = [os.path.join(PASTA_DOWNLOADS, f) for f in novos]
        caminhos = [c for c in caminhos if os.path.isfile(c)]
        if caminhos:
            return max(caminhos, key=os.path.getmtime)
    return None


def renomear_arquivo_final(caminho_atual, info, tipo):
    """
    Renomeia o arquivo salvo para um padrão limpo e curto.
    Exemplo:
    - facebook_1417545490408392.jpg
    - instagram_CxYz123.mp4
    """
    if not caminho_atual or not os.path.exists(caminho_atual):
        return caminho_atual

    ext = Path(caminho_atual).suffix.lower() or ".bin"

    extractor = "arquivo"
    media_id = "sem_id"

    if isinstance(info, dict):
        extractor = limpar_nome_arquivo(info.get("extractor") or info.get("extractor_key") or "arquivo")
        media_id = limpar_nome_arquivo(str(info.get("id") or "sem_id"))

    if tipo == "imagem":
        novo_nome = f"{extractor}_{media_id}{ext}"
    else:
        novo_nome = f"{extractor}_{media_id}{ext}"

    novo_caminho = os.path.join(PASTA_DOWNLOADS, novo_nome)

    contador = 1
    while os.path.exists(novo_caminho) and os.path.abspath(novo_caminho) != os.path.abspath(caminho_atual):
        base = f"{extractor}_{media_id}_{contador}"
        novo_caminho = os.path.join(PASTA_DOWNLOADS, f"{base}{ext}")
        contador += 1

    if os.path.abspath(caminho_atual) != os.path.abspath(novo_caminho):
        os.replace(caminho_atual, novo_caminho)

    return novo_caminho


def baixar_arquivo(url, tipo):
    """
    Executa o download e força renomeação limpa no final.
    """
    opcoes = montar_opcoes_ydl(tipo)
    arquivos_antes = set(os.listdir(PASTA_DOWNLOADS))

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)

    arquivos_depois = set(os.listdir(PASTA_DOWNLOADS))

    if isinstance(info, dict) and info.get("entries"):
        total = 0
        for entrada in info["entries"]:
            if not entrada:
                continue
            total += 1
        return f"✅ Download concluído. {total} arquivo(s) salvo(s) com sucesso."

    caminho_novo = encontrar_arquivo_recente(arquivos_antes, arquivos_depois)
    caminho_final = renomear_arquivo_final(caminho_novo, info, tipo)

    nome_final = os.path.basename(caminho_final) if caminho_final else "arquivo"
    return f"✅ Download concluído com sucesso: {nome_final}"


@app.route("/", methods=["GET", "POST"])
def index():
    """Rota principal."""
    mensagem = None

    if request.method == "POST":
        url = (request.form.get("url") or "").strip()
        tipo = (request.form.get("tipo") or "video").strip().lower()

        if not url:
            mensagem = "❌ Cole uma URL válida para iniciar o download."
        elif tipo not in {"video", "imagem"}:
            mensagem = "❌ Tipo de download inválido."
        else:
            try:
                mensagem = baixar_arquivo(url, tipo)
            except Exception as erro:
                mensagem = sanitizar_mensagem_erro(erro)

    arquivos = listar_arquivos()
    return render_template("index.html", mensagem=mensagem, arquivos=arquivos)


@app.route("/download/<path:filename>")
def download_file(filename):
    """Faz o download do arquivo salvo."""
    nome_seguro = os.path.basename(filename)
    return send_from_directory(PASTA_DOWNLOADS, nome_seguro, as_attachment=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "False") == "True"

    print(f"🌸 Pétala Hunter rodando na porta {port}")
    print("✅ Renomeação pós-download habilitada")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)