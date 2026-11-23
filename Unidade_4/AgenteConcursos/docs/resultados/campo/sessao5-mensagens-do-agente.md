# Sessão de OCR (PDF escaneado): mensagens

Sessão `sesn_01TDxo14Zbyd3B5sFDj8ve6m`. Texto exato devolvido pela API, sem edição.

## Pedido enviado

Teste de OCR. O arquivo /workspace/vault/_editais/edital-escaneado.pdf é uma digitalização sem camada de texto. Rode só extrair, segmentar e cobertura, numa pasta de trabalho nova em /workspace/vault/.concursos-work/teste-ocr. Não gere pasta de concurso. Responda com: páginas lidas por OCR, número de itens do corpo, disciplinas e tópicos do conteúdo programático, resultado da cobertura e os trechos que parecem erro de leitura e precisam de conferência no PDF.

## Resposta (16:14:20)

**Status**

| Verificação | Resultado |
|---|---|
| Cobertura | ✅ 100%. Conteúdo programático: 291 de 291 tokens. Corpo: 391 de 391 tokens. Nada faltando, inventado ou movido. |
| Citações | Não se aplica. Não foi gerada ficha. |
| Alertas de injeção | Nenhum. |
| Auditoria | ❌ 1 achado, em nota que já existia. Não foi criada por esta execução. |

Não abra `_validacao/Teste JS desligado.md` (linha 5) no Obsidian. Ela tem um bloco `dataviewjs` diferente dos do Painel, com o texto "JAVASCRIPT EXECUTOU". Não apaguei nem editei a nota.

**Páginas lidas por OCR:** 1, 2, 3 e 4. São todas as páginas do PDF, então todas precisam de conferência.

**Corpo do edital:** 23 itens (1, 1.1 a 1.3, 2, 2.1 a 2.1.4, 3, 3.1, 3.2, 4, 4.1 a 4.3, 5, 5.1 a 5.4 e 6).

**Conteúdo programático** (item 6, linhas 57 a 93 do texto)

| Grupo | Disciplina | Tópicos |
|---|---|---|
| 6.2.1 Conhecimentos básicos | Língua Portuguesa | 10 |
| 6.2.1 Conhecimentos básicos | Noções de Direito Constitucional | 5 |
| 6.2.1 Conhecimentos básicos | Legislação | 3 |
| 6.2.2 Específicos, Cargo 202 | Infraestrutura | 6 |
| 6.2.2 Específicos, Cargo 202 | Banco de Dados | 5 |

Total: 29 tópicos. As contagens batem com a numeração do texto, incluindo os subitens (4.1, 4.2, 5.1, 5.2, 3.1 e 2.1, 2.2).

Estrutura:
- O item 6.1 foi para `observacoes`.
- A assinatura ("FULANO DE TAL" e "Diretor-Presidente…") foi para `observacoes_finais`.

**Trechos com provável erro de leitura (conferir no PDF)**

| Pág. | Trecho lido | Provável correto | Observação |
|---|---|---|---|
| 1 | "de pone eliminatório" (item 1.2 a) | "porte" ou "peso" | Erro certo. Não é palavra do português. |
| 1 | "1.3.As provas" | "1.3 As provas" | Ponto espúrio. |
| 2 | "A nota-em cada item" (5.2) | "A nota em cada item" | Hífen espúrio. |
| 2 | "até à 150º posição" (5.4) | "até a 150ª posição" | Crase e ordinal suspeitos. Confira o número 150 no PDF. |
| 1 a 4 | Cabeçalhos "EDITAL N 1", "EDITAL.N 1- SEFIC/DF", "Pagina 2.de 4" | "EDITAL Nº 1", "Página 2 de 4" | Não afetam o corpo, porque foram removidos como cabeçalho. Mostram a qualidade do OCR. |
| 2 | Item 4.1: "conforme o quadro a seguir" | — | O quadro não apareceu no texto, e `tabelas.md` está vazio. Provavelmente foi perdido no OCR. Confira no PDF se existe e o que ele traz. |

Valores que o OCR pode ter trocado sem gerar palavra inválida. Confira todos no PDF antes de usá-los:
- Datas e prazos (3.1, 4.3): 20/07/2026 e 10/08/2026, 10h e 18h, e 12/10/2026.
- Valores em R$ (2.1.2, 3.2): R$ 6.500,00 e R$ 90,00.
- Vagas (2.1.3): 10, 1 PcD e 3 candidatos negros.
- Itens e mínimos (4.2, 5.3): 50 e 70 itens, mínimos de 10,00, 21,00 e 36,00.

Os mínimos são coerentes entre si: 10/50 = 20%, 21/70 = 30% e 36/120 = 30%. Isso reduz o risco de troca de dígito, mas não o elimina.

A cobertura compara o texto extraído com ele mesmo. Ela garante que nada se perdeu depois do OCR, e não que o OCR leu certo. Esses erros passaram pelo teste e continuam literais no verticalizado.

**Arquivos**
- Pasta de trabalho: `/workspace/vault/.concursos-work/teste-ocr/`
- Arquivos principais: `texto.txt`, `meta.json`, `itens.json`, `verticalizado.json`, `cobertura.md`
- Não foi criada pasta em `Concursos/`.

**Próximo passo:** abra o PDF e confira as 4 páginas contra a tabela acima, principalmente o quadro do item 4.1. Se quiser, eu aplico as correções como retificação literal (`retificacoes.json`) e refaço a segmentação e a cobertura.
