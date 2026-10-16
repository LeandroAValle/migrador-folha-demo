# Arquitetura

`source_rows()` cria 238 registros fictícios em quatro entidades. `validate_row()` verifica requisitos mínimos antes da transformação. `transform_row()` monta um payload genérico e preserva a chave de negócio. `simulate_provider()` fornece respostas locais reproduzíveis. `build_snapshot()` registra histórico por item, agrega indicadores por entidade e concilia totais. A CLI exporta JSON para o site.

```text
payroll_demo/pipeline.py  ->  site/data/snapshot.json  ->  site/app.js
          ^                                                  |
       tests/                                     painel no GitHub Pages
```

## Estados

Um registro válido percorre `EXTRAIDO → VALIDADO → PENDENTE → ENVIADO → EXECUTADO | ERRO`. Um registro inválido percorre `EXTRAIDO → VALIDADO → ERRO`, sem payload. `ENVIADO` significa apenas passagem pelo simulador offline. Não existe chamada HTTP para um fornecedor.

## Limites

O snapshot oferece visibilidade de resultados, não um controle operacional de migração. Não há banco, filas, credenciais, autenticação ou reprocessamento real. Uma solução de produção exigiria persistência transacional, contratos homologados, segurança, retomada idempotente e auditoria com acesso controlado.
