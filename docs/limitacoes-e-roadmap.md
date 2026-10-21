# Limitações e roadmap

## Limitações atuais

> **Importante:** a compatibilidade real depende da disponibilidade pública da URL, de mudanças nas plataformas e da versão do `yt-dlp` instalada.

Este projeto depende diretamente do comportamento do `yt-dlp` e da acessibilidade pública das URLs. Isso significa que mudanças nas plataformas podem impactar o funcionamento sem aviso prévio.

Pontos importantes:

- Nem toda URL pública continuará funcionando ao longo do tempo.
- Conteúdos privados, restritos ou protegidos por login podem falhar.
- Plataformas mudam seletores, endpoints e políticas com frequência.
- O suporte a carrosséis, imagens e vídeos pode variar por plataforma.

## Melhorias recomendadas

Para a próxima versão, estas evoluções tendem a gerar mais estabilidade e manutenibilidade:

- Separar a lógica de download da camada Flask.
- Criar serviços por plataforma.
- Mover configurações para variáveis de ambiente.
- Remover segredo fixo do código-fonte.
- Adicionar logs estruturados.
- Criar testes unitários para normalização, renomeação e tratamento de erros.
- Versionar melhor as capacidades por plataforma.
- Adicionar fila assíncrona para downloads mais pesados.

---

[← Voltar ao README](../README.md)
