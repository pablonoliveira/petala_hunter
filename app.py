from flask import Flask, request, render_template, send_from_directory, abort
import os
import re
from pathlib import Path
import yt_dlp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "petala-hunter-2026")

PASTA_DOWNLOADS = "downloads"
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

ARQUIVOS_SESSAO = []
DEBUG_LOGS = os.getenv("DEBUG_LOGS", "True") == "True"


def log_debug(msg):
    if DEBUG_LOGS:
        print(f"[PETALA_DEBUG] {msg}")


def listar_arquivos_sessao():
    arquivos_validos = []
    for nome in ARQUIVOS_SESSAO:
        caminho = os.path.join(PASTA_DOWNLOADS, nome)
        if os.path.isfile(caminho):
            arquivos_validos.append(nome)
    return arquivos_validos[::-1][:12]


def limpar_nome_arquivo(texto):
    texto = str(texto or "arquivo")
    texto = re.sub(r'[\\/*?:"<>|=&%#]+', "", texto)
    texto = re.sub(r"\s+", "_", texto).strip("_")
    return texto[:80] or "arquivo"


def detectar_plataforma(url):
    url = (url or "").lower()
    if "facebook.com/ads/library" in url or "facebook.com/ads" in url:
        return "Meta Ads Library"
    if "instagram.com" in url:
        return "Instagram"
    if "tiktok.com" in url:
        return "TikTok"
    if "facebook.com" in url:
        return "Facebook"
    return "Link externo"


def inferir_tipo_instagram(url):
    url = (url or "").lower()
    if "/reel/" in url:
        return "reel"
    if "/p/" in url:
        return "post"
    if "/stories/" in url:
        return "stories"
    return "desconhecido"


def sanitizar_mensagem_erro(erro, tipo=None, url=None):
    msg = str(erro)
    plataforma = detectar_plataforma(url)
    tipo_instagram = inferir_tipo_instagram(url)

    if "There is no video in this post" in msg:
        if plataforma == "Instagram" and tipo == "imagem" and tipo_instagram == "reel":
            return "❌ Esse link do Instagram parece ser um Reel. Para esse caso, tente o modo Vídeo/Reel."
        if plataforma == "Instagram" and tipo == "imagem":
            return "❌ Esse link do Instagram não disponibilizou imagem estática para extração no modo Foto/Post."
        return "❌ Esse post não possui vídeo disponível para o modo selecionado."

    if "Requested format is not available" in msg:
        if plataforma == "Instagram" and tipo == "imagem" and tipo_instagram == "reel":
            return "❌ Não foi encontrada imagem compatível para esse link. Como ele parece ser um Reel, tente o modo Vídeo/Reel."
        if tipo == "imagem":
            return "❌ Não foi encontrada uma imagem compatível para esse link no modo Foto/Post."
        return "❌ O formato solicitado não está disponível para esse link."

    if "facebook:ads" in msg and "Unable to extract ad data" in msg:
        return "❌ Não foi possível extrair os dados desse criativo da Meta Ads Library no momento."

    if "facebook:ads" in msg and "No video formats found" in msg:
        return "❌ Esse anúncio da Meta Ads Library não disponibilizou um vídeo baixável para o yt-dlp, mesmo após tentativa de fallback. Tente o modo Foto/Post, se o criativo não for vídeo."

    if "Unsupported URL" in msg:
        return "❌ Essa URL não é suportada pelo Pétala Hunter."

    if "Private video" in msg or "login required" in msg.lower():
        return "❌ O conteúdo exige autenticação ou não está acessível publicamente."

    if "ffmpeg" in msg.lower():
        return "❌ O FFmpeg parece não estar instalado ou acessível no sistema. Verifique a instalação para conteúdos que exigem processamento adicional."

    if "File name too long" in msg:
        return "❌ O nome do arquivo original era muito longo, mas o sistema tentou renomear automaticamente."

    return f"❌ Erro ao processar o link de {plataforma}: {msg[:180]}"


def montar_opcoes_ydl(tipo, formato_personalizado=None):
    nome_saida = os.path.join(PASTA_DOWNLOADS, "%(extractor)s_%(id)s.%(ext)s")
    opcoes = {
        "outtmpl": nome_saida,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": False,
        "extract_flat": False,
        "windowsfilenames": True,
        "restrictfilenames": True,
        "trim_file_name": 80,
    }

    if formato_personalizado:
        opcoes.update({"format": formato_personalizado})
    elif tipo == "imagem":
        opcoes.update({"format": "best[ext=jpg]/best[ext=jpeg]/best[ext=png]/best[ext=webp]/best[ext=bmp]/best[ext=gif]/best"})
    else:
        opcoes.update({"format": "best[ext=mp4]/best"})

    return opcoes


def snapshot_arquivos():
    dados = {}
    if not os.path.exists(PASTA_DOWNLOADS):
        return dados
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
    extractor = limpar_nome_arquivo(info.get("extractor_key") or info.get("extractor") or "arquivo")
    media_id = limpar_nome_arquivo(str(info.get("id") or "sem_id"))
    return f"{extractor}_{media_id}"


def registrar_na_sessao(nome_arquivo):
    if nome_arquivo and nome_arquivo not in ARQUIVOS_SESSAO:
        ARQUIVOS_SESSAO.append(nome_arquivo)
        log_debug(f"Arquivo registrado na sessão: {nome_arquivo}")


def renomear_arquivos_baixados(novos, info, tipo):
    if not novos:
        return []

    base_nome = montar_base_nome(info)
    renomeados = []
    extensoes_imagem = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
    extensoes_video = {".mp4", ".mkv", ".webm", ".mov"}

    arquivos_midia = []
    for caminho in novos:
        ext = Path(caminho).suffix.lower()
        if tipo == "imagem" and ext in extensoes_imagem:
            arquivos_midia.append(caminho)
        elif tipo == "video" and ext in extensoes_video:
            arquivos_midia.append(caminho)

    if tipo == "imagem" and not arquivos_midia:
        arquivos_midia = novos[:]
        log_debug("Fallback de imagem acionado: usando qualquer arquivo novo detectado.")

    if not arquivos_midia:
        return []

    for indice, caminho_atual in enumerate(arquivos_midia, start=1):
        ext = Path(caminho_atual).suffix.lower()
        if not ext:
            ext = ".bin" if tipo == "imagem" else ".mp4"

        novo_nome = f"{base_nome}{ext}" if len(arquivos_midia) == 1 else f"{base_nome}_{indice}{ext}"
        novo_nome = limpar_nome_arquivo(Path(novo_nome).stem) + ext
        novo_caminho = os.path.join(PASTA_DOWNLOADS, novo_nome)

        contador = 1
        while os.path.exists(novo_caminho) and os.path.abspath(novo_caminho) != os.path.abspath(caminho_atual):
            candidato = f"{base_nome}_{contador}{ext}" if len(arquivos_midia) == 1 else f"{base_nome}_{indice}_{contador}{ext}"
            candidato = limpar_nome_arquivo(Path(candidato).stem) + ext
            novo_caminho = os.path.join(PASTA_DOWNLOADS, candidato)
            contador += 1

        if os.path.abspath(caminho_atual) != os.path.abspath(novo_caminho):
            os.replace(caminho_atual, novo_caminho)
            log_debug(f"Arquivo renomeado: {os.path.basename(caminho_atual)} -> {os.path.basename(novo_caminho)}")

        nome_final = os.path.basename(novo_caminho)
        renomeados.append(nome_final)
        registrar_na_sessao(nome_final)

    return renomeados


def extrair_com_fallback(url, tipo, plataforma):
    tentativas = []

    if tipo == "video" and plataforma == "Meta Ads Library":
        tentativas = [
            ("padrao-meta", montar_opcoes_ydl(tipo, "best[ext=mp4]/best")),
            ("fallback-meta", montar_opcoes_ydl(tipo, "bestvideo+bestaudio/best")),
        ]
    else:
        tentativas = [("padrao", montar_opcoes_ydl(tipo))]

    ultimo_erro = None

    for nome_tentativa, opcoes in tentativas:
        try:
            log_debug(f"Tentativa de download: {nome_tentativa} | plataforma={plataforma} | tipo={tipo} | format={opcoes.get('format')}")
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
            log_debug(f"Tentativa bem-sucedida: {nome_tentativa}")
            return info
        except Exception as erro:
            ultimo_erro = erro
            log_debug(f"Falha na tentativa {nome_tentativa}: {erro}")

    raise ultimo_erro


def baixar_arquivo(url, tipo):
    plataforma = detectar_plataforma(url)
    antes = snapshot_arquivos()
    log_debug(f"Início do processamento | plataforma={plataforma} | tipo={tipo} | url={url}")
    log_debug(f"Arquivos antes: {list(antes.keys())}")

    info = extrair_com_fallback(url, tipo, plataforma)

    depois = snapshot_arquivos()
    log_debug(f"Arquivos depois: {list(depois.keys())}")
    novos = arquivos_novos(antes, depois)
    log_debug(f"Arquivos novos detectados: {[os.path.basename(a) for a in novos]}")

    renomeados = renomear_arquivos_baixados(novos, info, tipo)
    log_debug(f"Arquivos renomeados/finais: {renomeados}")

    if renomeados:
        if len(renomeados) == 1:
            return f"✅ Download concluído com sucesso: {renomeados[0]}"
        return f"✅ Download concluído com sucesso: {len(renomeados)} arquivos foram salvos nesta sessão."

    if novos:
        for caminho in novos:
            nome = os.path.basename(caminho)
            registrar_na_sessao(nome)
        if len(novos) == 1:
            return f"✅ Download concluído com sucesso: {os.path.basename(novos[0])}"
        return f"✅ Download concluído com sucesso: {len(novos)} arquivo(s) detectado(s) na sessão."

    raise RuntimeError("O link foi processado, mas nenhum arquivo compatível foi identificado para salvar nesta sessão.")


@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = None
    tipo_alerta = "info"
    url_atual = ""
    tipo_atual = "video"
    plataforma = None

    if request.method == "POST":
        url_atual = (request.form.get("url") or "").strip()
        tipo_atual = (request.form.get("tipo") or "video").strip().lower()
        plataforma = detectar_plataforma(url_atual)
        log_debug(f"POST recebido | tipo={tipo_atual} | plataforma={plataforma} | url={url_atual}")

        if not url_atual:
            mensagem = "❌ Cole uma URL válida para iniciar o download."
            tipo_alerta = "error"
        elif tipo_atual not in {"video", "imagem"}:
            mensagem = "❌ Tipo de download inválido."
            tipo_alerta = "error"
        else:
            try:
                mensagem = baixar_arquivo(url_atual, tipo_atual)
                tipo_alerta = "success"
            except Exception as erro:
                log_debug(f"Erro final tratado: {erro}")
                mensagem = sanitizar_mensagem_erro(erro, tipo_atual, url_atual)
                tipo_alerta = "error"
    else:
        mensagem = "Cole a URL de um criativo público da Meta Ads Library, Instagram, TikTok ou Facebook para iniciar o download."

    arquivos = listar_arquivos_sessao()
    return render_template(
        "index.html",
        mensagem=mensagem,
        tipo_alerta=tipo_alerta,
        arquivos=arquivos,
        url_atual=url_atual,
        tipo_atual=tipo_atual,
        plataforma=plataforma,
    )


@app.route("/download/<path:filename>")
def download_file(filename):
    nome_seguro = os.path.basename(filename)
    if nome_seguro not in ARQUIVOS_SESSAO:
        abort(404)
    return send_from_directory(PASTA_DOWNLOADS, nome_seguro, as_attachment=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "False") == "True"
    print(f"🌸 Pétala Hunter rodando na porta {port}")
    print(f"✅ Controle de downloads por sessão ativado | DEBUG_LOGS={DEBUG_LOGS}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
