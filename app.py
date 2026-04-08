from flask import Flask, request, render_template, send_from_directory
import os
import re
import yt_dlp

app = Flask(__name__)
app.config["SECRET_KEY"] = "creativehunter-2026"

PASTA_DOWNLOADS = "downloads"
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)


def listar_arquivos():
    if not os.path.exists(PASTA_DOWNLOADS):
        return []

    arquivos = [
        f for f in os.listdir(PASTA_DOWNLOADS)
        if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))
    ]
    return sorted(arquivos, reverse=True)[:12]


def sanitizar_mensagem_erro(erro):
    msg = str(erro)

    if "There is no video in this post" in msg:
        return "❌ Esse post não possui vídeo disponível para o modo selecionado."

    if "facebook:ads" in msg and "Unable to extract ad data" in msg:
        return "❌ Esse criativo da Meta Ads Library não pôde ser extraído pela versão atual do yt-dlp."

    if "Unsupported URL" in msg:
        return "❌ Essa URL não é suportada pelo CreativeHunter."

    if "Private video" in msg or "login required" in msg.lower():
        return "❌ O conteúdo exige autenticação ou não está acessível publicamente."

    return f"❌ Erro ao processar o link: {msg[:160]}"


def limpar_nome_arquivo(texto):
    texto = texto or "arquivo"
    texto = re.sub(r'[\\/*?:"<>|]', "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto[:120]


def montar_opcoes_ydl(tipo):
    nome_saida = os.path.join(
        PASTA_DOWNLOADS,
        "%(extractor)s_%(id)s.%(ext)s"
    )

    opcoes_base = {
        "outtmpl": nome_saida,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": False,
        "extract_flat": False,
        "windowsfilenames": True,
        "restrictfilenames": True,
    }

    if tipo == "imagem":
        opcoes_base.update({
            "format": "best[ext=jpg]/best[ext=jpeg]/best[ext=png]/best"
        })
    else:
        opcoes_base.update({
            "format": "bestvideo[height<=1080]+bestaudio/best"
        })

    return opcoes_base

def baixar_arquivo(url, tipo):
    opcoes = montar_opcoes_ydl(tipo)

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)

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

    print(f"🔥 CreativeHunter rodando na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)