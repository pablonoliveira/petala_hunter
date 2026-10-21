# -*- coding: utf-8 -*-
r"""
Pétala Hunter — download em lote de criativos da Biblioteca de Anúncios da Meta.

Lê dois arquivos de configuração (fora do git, ver .gitignore):
  clientes.json     -> pasta raiz no Google Drive para Desktop e a pasta de cada cliente
  referencias.json  -> lista de anúncios a baixar (cliente, anunciante, ID da Biblioteca)
Modelos com dados fictícios: clientes.exemplo.json e referencias.exemplo.json.

Cada vídeo é salvo em <raiz>\<pasta do cliente>\<subpasta>\<MÊS>\<Anunciante>_<ID>.mp4

Uso (na pasta do projeto, com o venv ativo):
    python baixar_referencias.py                 # baixa tudo
    python baixar_referencias.py --teste 3       # só os 3 primeiros
    python baixar_referencias.py --mes NOVEMBRO --pausa 8

Arquivos já baixados são pulados: rode de novo para tentar só os que falharam.
Ao final gera log_download_<data>.csv com o status de cada anúncio.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time

import yt_dlp

MESES = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO",
         "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
ESPERAS_429 = [60, 120, 240]  # segundos de espera quando o Facebook responde "Too Many Requests"


class _Silencioso:
    """Esconde as mensagens do yt-dlp; o resultado aparece na linha OK/ERRO e no log."""
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def carregar_json(caminho, exemplo):
    if not os.path.isfile(caminho):
        sys.exit(f"Arquivo não encontrado: {caminho}\n"
                 f"Copie '{exemplo}' para '{os.path.basename(caminho)}' e preencha com os seus dados.")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def limpar(texto):
    texto = re.sub(r'[\\/*?:"<>|=&%#@!\']+', "", str(texto))
    texto = re.sub(r"\s+", "_", texto).strip("_.")
    return texto[:50] or "anuncio"


def ja_baixado(pasta, base):
    if not os.path.isdir(pasta):
        return None
    for nome in os.listdir(pasta):
        if nome.startswith(base + ".") and not nome.endswith((".part", ".ytdl")):
            return nome
    return None


def baixar(url, destino_sem_ext):
    formatos = ["best[ext=mp4]/best", "bestvideo*+bestaudio/best"]
    ultimo = None
    for espera in [0] + ESPERAS_429:
        if espera:
            print(f"      Facebook limitou as requisições (429). Aguardando {espera}s e tentando de novo...")
            time.sleep(espera)
        bloqueado = False
        for fmt in formatos:
            opcoes = {
                "outtmpl": destino_sem_ext + ".%(ext)s",
                "format": fmt,
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "windowsfilenames": True,
                "retries": 3,
                "merge_output_format": "mp4",
                "logger": _Silencioso(),
            }
            try:
                with yt_dlp.YoutubeDL(opcoes) as ydl:
                    ydl.extract_info(url, download=True)
                return None
            except Exception as erro:  # noqa: BLE001
                ultimo = erro
                if "429" in str(erro):
                    bloqueado = True
                    break
        if not bloqueado:
            break  # erro que não é de limite (ex.: anúncio não extraível): não adianta esperar
    return str(ultimo)[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clientes", default="clientes.json", help="config com raiz e pastas dos clientes")
    ap.add_argument("--referencias", default="referencias.json", help="lista de anúncios a baixar")
    ap.add_argument("--raiz", help="sobrescreve a pasta raiz definida em clientes.json")
    ap.add_argument("--mes", default=MESES[dt.date.today().month - 1], help="nome da subpasta do mês")
    ap.add_argument("--teste", type=int, default=0, help="baixa só N anúncios para testar")
    ap.add_argument("--pausa", type=float, default=6.0, help="segundos entre downloads")
    args = ap.parse_args()

    config = carregar_json(args.clientes, "clientes.exemplo.json")
    referencias = carregar_json(args.referencias, "referencias.exemplo.json")
    raiz = args.raiz or config["raiz"]
    clientes = config["clientes"]

    if not os.path.isdir(raiz):
        sys.exit(f"Pasta raiz não encontrada: {raiz}\n"
                 "Confira se o Google Drive para Desktop está aberto e sincronizando.")

    sem_pasta = sorted({r["cliente"] for r in referencias if r["cliente"] not in clientes})
    if sem_pasta:
        sys.exit("Clientes sem pasta definida em clientes.json: " + ", ".join(sem_pasta))

    print(f"yt-dlp {yt_dlp.version.__version__} | raiz: {raiz} | mês: {args.mes}")
    lista = referencias[: args.teste] if args.teste else referencias
    log = []
    ok = pulados = erros = 0

    for n, ref in enumerate(lista, 1):
        cliente, anunciante, ad_id = ref["cliente"], ref["anunciante"], str(ref["id"])
        cfg = clientes[cliente]
        pasta = os.path.join(raiz, cfg["pasta"], cfg.get("subpasta", "Pesquisa de Anúncios"), args.mes)
        os.makedirs(pasta, exist_ok=True)
        base = f"{cfg.get('prefixo', '')}{limpar(anunciante)}_{ad_id}"
        url = f"https://www.facebook.com/ads/library/?id={ad_id}"

        existente = ja_baixado(pasta, base)
        if existente:
            pulados += 1
            status, detalhe = "JA_EXISTIA", existente
        else:
            erro = baixar(url, os.path.join(pasta, base))
            if erro:
                erros += 1
                status, detalhe = "ERRO", erro
            else:
                ok += 1
                status, detalhe = "OK", ja_baixado(pasta, base) or base
            time.sleep(args.pausa)

        print(f"[{n:02d}/{len(lista)}] {status:10} {cliente} | {anunciante} | {ad_id}")
        log.append([cliente, anunciante, ad_id, url, status, detalhe, pasta])

    nome_log = f"log_download_{dt.datetime.now():%Y-%m-%d_%H%M}.csv"
    with open(nome_log, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Cliente", "Anunciante", "ID", "Link", "Status", "Arquivo/Erro", "Pasta"])
        w.writerows(log)

    print(f"\nConcluído: {ok} baixados, {pulados} já existiam, {erros} com erro. Log: {nome_log}")
    if erros:
        print("Erros 429: espere 20–30 min e rode de novo (os já baixados são pulados).")
        print("'Unable to extract ad data': baixe esse anúncio manualmente pelo link do log.")


if __name__ == "__main__":
    main()
