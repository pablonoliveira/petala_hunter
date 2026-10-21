# Segurança e deploy

## Segurança

Antes de publicar uma nova versão, é recomendável:

- substituir a `SECRET_KEY` fixa por variável de ambiente;
- validar tamanho e formato das URLs recebidas;
- limitar concorrência e volume de downloads;
- revisar exposição pública da pasta `downloads`;
- registrar falhas sem vazar detalhes sensíveis ao usuário final.

## Deploy

Por ser um projeto Flask enxuto, o Pétala Hunter pode ser executado localmente, em VPS, contêiner Docker ou plataformas de deploy compatíveis com Python. Em ambientes de produção, é recomendável usar um servidor WSGI como Gunicorn e persistência adequada para a pasta de downloads.

Exemplo com Gunicorn:

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

[← Voltar ao README](../README.md)
