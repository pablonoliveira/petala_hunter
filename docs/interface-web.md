# Interface web

Como funciona o download individual pela interface Flask.

O projeto usa **Flask** para a interface web e **yt-dlp** como motor de extração. Quando necessário, os arquivos baixados passam por um processo de renomeação inteligente para facilitar organização, especialmente em casos com múltiplos itens no mesmo conteúdo. A interface também lista os downloads mais recentes e mostra mensagens de erro amigáveis.

## Como funciona

1. O usuário cola uma URL pública no formulário.
2. Escolhe o modo de download: `video` ou `imagem`.
3. A aplicação monta as opções do `yt-dlp` conforme o tipo selecionado (no TikTok, com impersonação de navegador).
4. O conteúdo é baixado para a pasta `downloads/`.
   - No modo `imagem`, se o link não tiver vídeo, entra o **fallback de imagem estática** (veja abaixo).
5. Os arquivos recém-gerados são identificados e renomeados com base no extrator e no ID da mídia.
6. A interface exibe a mensagem de resultado e a lista de arquivos recentes.

## Fallback de imagem estática

O `yt-dlp` foi feito para vídeo: em posts de foto do Instagram e anúncios em imagem da Meta Ads Library ele responde "There is no video in this post" ou "No video formats found". Nesses casos, no modo `imagem`, o app:

1. Extrai os dados do link sem baixar (`ignore_no_formats_error`).
2. Escolhe a maior imagem de cada item (`display_url`, `original_image_url` ou a maior miniatura).
3. **Meta Ads Library:** lê as imagens direto dos dados do anúncio (`snapshot.images` e `snapshot.cards`), reaproveitando o extrator do `yt-dlp` para passar pela verificação do Facebook.
4. Salva cada imagem (carrosséis geram `_1`, `_2`…) e aplica a renomeação padrão.

Funções no `app.py`: `baixar_imagens_estaticas`, `coletar_urls_imagens`, `imagens_meta_ads`, `melhor_imagem`.

## TikTok e impersonação

O TikTok bloqueia requisições que não parecem vir de um navegador. Com o pacote `curl_cffi` instalado, o app passa `impersonate=chrome` ao `yt-dlp` **apenas** para o TikTok (`PLATAFORMAS_COM_IMPERSONATE`). Sem o pacote, o app continua funcionando nas demais plataformas.

## Organização dos downloads

Os arquivos são salvos na pasta `downloads/` e passam por normalização de nome. O padrão usa o extrator e o identificador da mídia como base, o que ajuda a evitar nomes longos, caracteres inválidos e colisões simples entre arquivos.

Exemplos de nomenclatura:

```text
facebook_123456789.mp4
instagram_ABCDEF123.jpg
tiktok_987654321_1.jpg
```

## Tratamento de erros

A aplicação já trata alguns cenários comuns com mensagens mais amigáveis, por exemplo:

- URL não suportada
- Conteúdo privado ou com autenticação
- Post sem vídeo no modo selecionado (com fallback automático no modo `imagem`)
- Falha de extração na Meta Ads Library
- Nome de arquivo excessivamente longo

---

[← Voltar ao README](../README.md)
