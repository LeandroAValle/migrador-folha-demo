# Decisões técnicas

| Decisão | Motivo | Consequência |
| --- | --- | --- |
| Criar repositório novo e independente | O original contém credenciais e regras operacionais | Histórico e código privados permanecem privados |
| Usar GitHub Pages como estudo de caso | Mostrar somente identidade e conteúdo que representam o projeto original | Simulador interativo fica local e claramente separado |
| Gerar dados com semente fixa | Permitir revisão e testes consistentes | A amostra não representa uma folha real |
| Simular respostas por registro | Expor o tratamento de sucesso e erro | Não comprova compatibilidade com API externa |
| Bloquear inválidos antes do payload | Tornar falha de qualidade visível | Registro inválido permanece em `ERRO` |
| Preservar chave de negócio | Relacionar origem e destino demonstrativo | Chave técnica do fornecedor não é usada |
| Conciliação obrigatória | Evitar perda silenciosa na amostra | Toda extração termina em executado ou revisão |

O envio é **simulado**; não afirmar que o projeto migra dados reais ou implementa o contrato da Betha Cloud. O fluxo ilustra decisões de engenharia baseadas no problema, sem copiar o sistema privado.
