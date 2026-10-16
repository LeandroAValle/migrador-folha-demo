# Dados e métricas

O dataset é 100% sintético e não inclui nomes, CPF, matrícula real, endereço ou dados bancários. Entidades: Servidor, Vínculo, Rubrica e Lançamento. Unidades Aurora, Horizonte e Vale são fictícias. O período é setembro de 2026.

| Campo | Significado |
| --- | --- |
| `sourceKey` | Identificador estável criado para o demo |
| `entity` | Categoria ilustrativa do registro |
| `requiredCode` | Código genérico usado pela validação |
| `payload` | Dados transformados em formato genérico; `null` se inválido |
| `history` | Estados percorridos pelo registro |
| `message` | Resultado da simulação ou motivo de bloqueio |

| Métrica | Regra |
| --- | --- |
| Extraídos | Total de registros gerados na origem fictícia |
| Validados para envio | Registros que passaram na validação |
| Executados | Registros aceitos pelo simulador |
| Para revisão | Registros inválidos ou rejeitados pelo simulador |
| Lotes simulados | Arredondamento para cima de `validados ÷ 25` |

`extraídos = executados + para revisão`. As contagens por entidade reconciliam com o total.
