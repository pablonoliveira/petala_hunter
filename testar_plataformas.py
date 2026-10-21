# -*- coding: utf-8 -*-
r"""
Pétala Hunter — teste de compatibilidade por plataforma.

Usa as MESMAS opções do app.py (montar_opcoes_ydl + fallback da Meta Ads Library)
para verificar se cada plataforma/modo ainda funciona com o yt-dlp instalado.

Links de teste: testes_plataformas.json (fora do git). Modelo: testes_plataformas.exemplo.json
    [
      {"plataforma": "Instagram", "modo": "video",  "url": "https://www.instagram.com/reel/..."},
      {"plataforma": "Instagram", "modo": "imagem", "url": "https://www.instagram.com/p/..."}
    ]

Uso (na pasta do projeto, com o venv ativo):
    python testar_plataformas.py            # simulação: extrai e escolhe o formato, sem baixar
    python testar_plataformas.py --baixar   # baixa de verdade numa pasta temporária e apaga no fim

Gera teste_plataformas_<data>.csv e mostra um resumo por plataforma.
"""
import argparse
import csv
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import time

import yt_dlp

try:
    import app  # reaproveita a configuração real da interface web
except Exception as erro:  # noqa: BLE001
    sys.exit(f"Não foi possível importar o app.py ({erro}). Rode este script na pasta do petala_hunter, com o venv ativo.")

ARQ_TESTES = "testes_plataformas.json"
MODOS_VALIDOS = {"video", "imagem"}


class _Silencioso:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def tentativas_do_app(tipo, plataforma):
    """Mesma ordem de tentativas de app.extrair_com_fallback."""
    if tipo == "video" and plataforma == "Meta Ads Library":
        return [("padrao-meta", "best[ext=mp4]/best"), ("fallback-meta", "bestvideo+bestaudio/best")]
    return [("padrao", None)]


def _opcoes(tipo, formato, plataforma, pasta_tmp):
    opcoes = app.montar_opcoes_ydl(tipo, formato, plataforma)
    opcoes.update({"logger": _Silencioso(), "quiet": True, "no_warnings": True})
    opcoes["outtmpl"] = os.path.join(pasta_tmp, "%(extractor)s_%(id)s.%(ext)s")
    return opcoes


def simular(url, tipo, plataforma, pasta_tmp):
    """Extrai sem baixar, seguindo a mesma lógica do app (incluindo o fallback de imagem estática)."""
    ultimo = None
    for nome, formato in tentativas_do_app(tipo, plataforma):
        try:
            with yt_dlp.YoutubeDL(_opcoes(tipo, formato, plataforma, pasta_tmp)) as ydl:
                info = ydl.extract_info(url, download=False)
            itens = [i for i in (info.get("entries") or [info]) if i]
            return info, itens, nome
        except Exception as erro:  # noqa: BLE001
            ultimo = erro
    if tipo == "imagem" and any(t in str(ultimo) for t in app.ERROS_SEM_VIDEO):
        opcoes = _opcoes(tipo, None, plataforma, pasta_tmp)
        opcoes.update({"ignore_no_formats_error": True, "skip_download": True})
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=False)
            urls = app.coletar_urls_imagens(ydl, url, plataforma, info)
        if not urls:
            raise RuntimeError("Nenhuma imagem encontrada neste link.")
        return info, [{"ext": "img"}] * len(urls), "imagem-estatica"
    raise ultimo


def testar(url, tipo, baixar, pasta_tmp):
    plataforma = app.detectar_plataforma(url)
    inicio = time.time()
    try:
        if baixar:
            # caminho real da interface web: app.baixar_arquivo salvando numa pasta temporária
            app.PASTA_DOWNLOADS = pasta_tmp
            app.ARQUIVOS_SESSAO.clear()
            mensagem = app.baixar_arquivo(url, tipo)
            arquivos = sorted(os.listdir(pasta_tmp))
            exts = sorted({os.path.splitext(a)[1] for a in arquivos})
            for f in arquivos:
                os.remove(os.path.join(pasta_tmp, f))
            if not arquivos:
                raise RuntimeError("nenhum arquivo foi salvo")
            detalhe = {"tentativa": "download", "extrator": plataforma, "itens": len(arquivos),
                       "ext": "/".join(e.lstrip(".") for e in exts), "resolucao": "",
                       "segundos": round(time.time() - inicio, 1)}
            return "OK", plataforma, detalhe, ""
        info, itens, nome = simular(url, tipo, plataforma, pasta_tmp)
        primeiro = itens[0] if itens else info
        detalhe = {
            "tentativa": nome,
            "extrator": info.get("extractor_key") or info.get("extractor"),
            "itens": len(itens),
            "ext": "img" if nome == "imagem-estatica" else primeiro.get("ext"),
            "resolucao": primeiro.get("resolution") or (f"{primeiro.get('width')}x{primeiro.get('height')}" if primeiro.get("width") else ""),
            "segundos": round(time.time() - inicio, 1),
        }
        return "OK", plataforma, detalhe, ""
    except Exception as erro:  # noqa: BLE001
        amigavel = app.sanitizar_mensagem_erro(erro, tipo, url)
        return "ERRO", plataforma, {}, f"{amigavel} | bruto: {str(erro)[:200]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arquivo", default=ARQ_TESTES, help="JSON com os links de teste")
    ap.add_argument("--baixar", action="store_true", help="baixa de verdade (numa pasta temporária, apagada no fim)")
    ap.add_argument("--pausa", type=float, default=4.0, help="segundos entre testes")
    args = ap.parse_args()

    if not os.path.isfile(args.arquivo):
        sys.exit(f"Arquivo não encontrado: {args.arquivo}\n"
                 "Copie 'testes_plataformas.exemplo.json' para 'testes_plataformas.json' e cole os links.")
    with open(args.arquivo, encoding="utf-8") as f:
        testes = json.load(f)

    invalidos = [t for t in testes if t.get("modo") not in MODOS_VALIDOS or not t.get("url")]
    if invalidos:
        sys.exit(f"Itens inválidos (modo deve ser 'video' ou 'imagem' e url preenchida): {invalidos}")

    imp = "ativa" if app.IMPERSONATE_ALVO is not None else "INATIVA (pip install curl_cffi)"
    print(f"yt-dlp {yt_dlp.version.__version__} | impersonação TikTok: {imp} | modo: {'download real' if args.baixar else 'simulação'} | {len(testes)} testes\n")
    pasta_tmp = tempfile.mkdtemp(prefix="petala_teste_")
    linhas = []
    try:
        for n, t in enumerate(testes, 1):
            if "COLE_AQUI" in t["url"]:
                rotulo = t.get("plataforma") or app.detectar_plataforma(t["url"])
                print(f"[{n:02d}/{len(testes)}] PULADO {rotulo:18} {t['modo']:7} link ainda não preenchido em {args.arquivo}")
                linhas.append([rotulo, "", t["modo"], t["url"], "PULADO", "", "", "", "", "", "link não preenchido"])
                continue
            status, plataforma, det, erro = testar(t["url"], t["modo"], args.baixar, pasta_tmp)
            rotulo = t.get("plataforma") or plataforma
            info = f"{det.get('extrator')} | {det.get('itens')} item(ns) | {det.get('ext')} {det.get('resolucao')} | {det.get('segundos')}s" if det else erro
            print(f"[{n:02d}/{len(testes)}] {status:5} {rotulo:18} {t['modo']:7} {info}")
            linhas.append([rotulo, plataforma, t["modo"], t["url"], status,
                           det.get("tentativa", ""), det.get("extrator", ""), det.get("itens", ""),
                           det.get("ext", ""), det.get("resolucao", ""), erro])
            if n < len(testes):
                time.sleep(args.pausa)
    finally:
        shutil.rmtree(pasta_tmp, ignore_errors=True)

    nome = f"teste_plataformas_{dt.datetime.now():%Y-%m-%d_%H%M}.csv"
    with open(nome, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Plataforma", "Detectada pelo app", "Modo", "URL", "Status", "Tentativa",
                    "Extrator", "Itens", "Extensão", "Resolução", "Erro"])
        w.writerows(linhas)

    print("\nResumo por plataforma:")
    resumo = {}
    for l in linhas:
        resumo.setdefault((l[0], l[2]), []).append(l[4])
    for (plat, modo), st in resumo.items():
        testados = [x for x in st if x != "PULADO"]
        if not testados:
            print(f"  ⏸️  {plat:18} {modo:7} sem link")
            continue
        ok = testados.count("OK")
        marca = "✅" if ok == len(testados) else ("⚠️" if ok else "❌")
        print(f"  {marca} {plat:18} {modo:7} {ok}/{len(testados)} OK")
    print(f"\nRelatório: {nome}")


if __name__ == "__main__":
    main()
