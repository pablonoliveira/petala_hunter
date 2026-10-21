# Interface web

Como funciona o download individual pela interface Flask.

## Como funciona

1. O usuário cola uma URL pública no formulário.
2. Escolhe o modo de download: `video` ou `imagem`.
3. A aplicação monta as opções do `yt-dlp` conforme o tipo selecionado.
4. O conteúdo é baixado para a pasta `downloads/`.
5. Os arquivos recém-gerados são identificados e renomeados com base no extrator e no ID da mídia.
6. A interface exibe a mensagem de resultado e a lista de arquivos recentes.

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
- Post sem vídeo no modo selecionado
- Falha de extração na Meta Ads Library
- Nome de arquivo excessivamente longo

---

[← Voltar ao README](../README.md)
