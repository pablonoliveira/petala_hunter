"""
Pétala Hunter - Captador de Criativos para Meta Ads, Reels e TikTok
Download automático em máxima qualidade + RENOMEAÇÃO PERFEITA.

Versão PROD: Flask + yt-dlp com renomeação inteligente de carrossel.
Resolve TODOS os casos: foto única, múltiplas fotos, vídeos.
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
    if not os.path.exists(PASTA_DOWNLOADS):
        return []

    arquivos = [
        f for f in os.listdir(PASTA_DOWNLOADS)
        if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
    ]
    arquivos.sort(key=lambda f: os.path.getmtime(os.path.join(PASTA_DOWNLOADS, f)), reverse=True)
    return arquivos[:12]


def sanitizar_mensagem_erro(erro):
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
        return "❌ Nome do arquivo muito longo. O app agora renomeia automaticamente."

    return f"❌ Erro ao processar o link: {msg[:160]}"


def limpar_nome_arquivo(texto):
    texto = texto or "arquivo"
    texto = str(texto)
    texto = re.sub(r'[\\/*?:"<>|=&%#]+', "", texto)
    texto = re.sub(r"\s+", "_", texto).strip("_")
    return texto[:80] or "arquivo"


def montar_opcoes_ydl(tipo):
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


def snapshot_arquivos():
    if not os.path.exists(PASTA_DOWNLOADS):
        return {}
    dados = {}
    for nome in os.listdir(PASTA_DOWNLOADS):
        caminho = os.path.join(PASTA_DOWNLOADS, nome)
        if os.path.isfile(caminho):
            dados[nome] = os.path.getmtime(caminho)
    return dados


def arquivos_novos(antes, depois):
    novos = []

    for nome, mtime in depois.items():
        if nome not in antes or antes[nome] != mtime:
            caminho = os.path.join(PASTA_DOWNLOADS, nome)
            if os.path.isfile(caminho):
                novos.append(caminho)

    novos.sort(key=os.path.getmtime)
    return novos


def montar_base_nome(info):
    if not isinstance(info, dict):
        return "arquivo_sem_id"

    extractor = limpar_nome_arquivo(
        info.get("extractor_key") or info.get("extractor") or "arquivo"
    )
    media_id = limpar_nome_arquivo(str(info.get("id") or "sem_id"))

    return f"{extractor}_{media_id}"


def renomear_arquivos_baixados(novos, info, tipo):
    if not novos:
        return []

    base_nome = montar_base_nome(info)
    renomeados = []

    extensoes_imagem = {".jpg", ".jpeg", ".png", ".webp"}
    extensoes_video = {".mp4", ".mkv", ".webm", ".mov"}

    arquivos_midia = []
    for caminho in novos:
        ext = Path(caminho).suffix.lower()
        if tipo == "imagem" and ext in extensoes_imagem:
            arquivos_midia.append(caminho)
        elif tipo == "video" and ext in extensoes_video:
            arquivos_midia.append(caminho)

    if not arquivos_midia:
        return []

    for indice, caminho_atual in enumerate(arquivos_midia, start=1):
        ext = Path(caminho_atual).suffix.lower()

        if len(arquivos_midia) == 1:
            novo_nome = f"{base_nome}{ext}"
        else:
            novo_nome = f"{base_nome}_{indice}{ext}"

        novo_nome = limpar_nome_arquivo(Path(novo_nome).stem) + ext
        novo_caminho = os.path.join(PASTA_DOWNLOADS, novo_nome)

        contador = 1
        while os.path.exists(novo_caminho) and os.path.abspath(novo_caminho) != os.path.abspath(caminho_atual):
            if len(arquivos_midia) == 1:
                candidato = f"{base_nome}_{contador}{ext}"
            else:
                candidato = f"{base_nome}_{indice}_{contador}{ext}"

            candidato = limpar_nome_arquivo(Path(candidato).stem) + ext
            novo_caminho = os.path.join(PASTA_DOWNLOADS, candidato)
            contador += 1

        if os.path.abspath(caminho_atual) != os.path.abspath(novo_caminho):
            os.replace(caminho_atual, novo_caminho)

        renomeados.append(os.path.basename(novo_caminho))

    return renomeados


def baixar_arquivo(url, tipo):
    antes = snapshot_arquivos()
    opcoes = montar_opcoes_ydl(tipo)

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)

    depois = snapshot_arquivos()
    novos = arquivos_novos(antes, depois)
    renomeados = renomear_arquivos_baixados(novos, info, tipo)

    if renomeados:
        if len(renomeados) == 1:
            return f"✅ Download concluído com sucesso: {renomeados[0]}"
        return f"✅ Download concluído com sucesso: {len(renomeados)} arquivos renomeados"

    if isinstance(info, dict) and info.get("entries"):
        total = len([item for item in info["entries"] if item])
        return f"✅ Download concluído. {total} arquivo(s) salvo(s) com sucesso."

    titulo = limpar_nome_arquivo(info.get("title")) if isinstance(info, dict) else "arquivo"
    return f"✅ Download concluído com sucesso: {titulo}"


@app.route("/", methods=["GET", "POST"])
def index():
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
    nome_seguro = os.path.basename(filename)
    return send_from_directory(PASTA_DOWNLOADS, nome_seguro, as_attachment=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "False") == "True"

    print(f"🌸 Pétala Hunter rodando na porta {port}")
    print("✅ Renomeação pós-download ativada")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)