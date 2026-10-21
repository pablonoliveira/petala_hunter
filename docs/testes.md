# Teste por plataforma

O `testar_plataformas.py` verifica se cada plataforma e modo (vídeo/imagem) ainda funciona com o `yt-dlp` instalado. Ele importa o `app.py` e usa **as mesmas opções da interface web**, então o resultado reflete o app de verdade.

Rode depois de atualizar o `yt-dlp` ou quando algum download começar a falhar.

## 1. Montar a lista de links

```bash
copy testes_plataformas.exemplo.json testes_plataformas.json
```

```json
[
  { "plataforma": "Meta Ads Library", "modo": "video",  "url": "https://www.facebook.com/ads/library/?id=..." },
  { "plataforma": "Meta Ads Library", "modo": "imagem", "url": "https://www.facebook.com/ads/library/?id=..." },
  { "plataforma": "Instagram",        "modo": "video",  "url": "https://www.instagram.com/reel/.../" },
  { "plataforma": "Instagram",        "modo": "imagem", "url": "https://www.instagram.com/p/.../" },
  { "plataforma": "TikTok",           "modo": "video",  "url": "https://www.tiktok.com/@perfil/video/..." },
  { "plataforma": "Facebook",         "modo": "video",  "url": "https://www.facebook.com/reel/..." }
]
```

- `modo`: `video` ou `imagem`.
- Use links **públicos**. Itens com `COLE_AQUI` na URL são pulados.
- `testes_plataformas.json` fica fora do git.

## 2. Executar

```powershell
.\TESTAR_PLATAFORMAS.bat            # simulação: extrai e escolhe o formato, sem baixar
.\TESTAR_PLATAFORMAS.bat --baixar   # download real (caminho da interface web) numa pasta temporária
```

| Opção | Padrão | Descrição |
|---|---|---|
| `--arquivo` | `testes_plataformas.json` | Lista de links |
| `--baixar` | desligado | Baixa de verdade com `app.baixar_arquivo` e apaga no fim |
| `--pausa` | `4` | Segundos entre testes |

A primeira linha mostra a versão do `yt-dlp` e se a impersonação do TikTok está **ativa**. Se aparecer `INATIVA`, instale o `curl_cffi` no venv: `python -m pip install curl_cffi`.

## 3. Ler o resultado

```text
Resumo por plataforma:
  ✅ Meta Ads Library   video   1/1 OK
  ✅ Meta Ads Library   imagem  1/1 OK
  ✅ Instagram          video   1/1 OK
  ✅ Instagram          imagem  1/1 OK
  ✅ TikTok             video   1/1 OK
  ✅ Facebook           video   1/1 OK
```

- ✅ todos OK · ⚠️ parte OK · ❌ todos falharam · ⏸️ sem link.
- O detalhe de cada teste (extrator, itens, extensão, erro amigável e erro bruto) vai para `teste_plataformas_<data>.csv`, também fora do git.
- Na coluna de extensão, `img` indica que o item foi resolvido pelo **fallback de imagem estática**.

## Erros comuns

| Mensagem | Causa provável | O que fazer |
|---|---|---|
| `Unexpected response from webpage request` (TikTok) | Proteção anti-robô | Instalar/atualizar `curl_cffi` |
| `No video formats found` / `There is no video in this post` | Link só com imagem testado em modo `video` | Testar em modo `imagem` |
| `HTTP Error 429` | Muitas requisições seguidas | Aguardar 20–30 min e aumentar `--pausa` |
| `Unable to extract ad data` | Formato de anúncio não suportado pelo `yt-dlp` | Trocar o link ou baixar manualmente |

---

[← Voltar ao README](../README.md)
