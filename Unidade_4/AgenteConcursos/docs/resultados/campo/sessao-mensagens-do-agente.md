# Sessão real: mensagens do agente

Sessão `sesn_01NjucVhopBAyHbvnmw1FWfK`. Texto exato devolvido pela API, sem edição.

## Mensagem 1 (13:09:41)

Perfil não existe (suposição a registrar). Leio a skill.

## Mensagem 2 (13:11:17)

**Status:** cobertura ✅ 100%, citações ✅, alertas de injeção nenhum, páginas por OCR nenhuma (as 4 páginas tinham texto). O ambiente está confirmado: `/workspace` tem `skills` e `vault`, e a skill `agente-concursos` está presente com o `concurso.py`. A pasta `Concursos/SEFIC-DF 2026 - Analista TI` ficou intacta, com data de modificação de 11:04, anterior a esta sessão.

**1. Cobertura**

| Alvo | Resultado |
|---|---|
| Conteúdo programático → `verticalizado.json` | 291 de 291 palavras preservadas, 0 faltando, 0 alteradas |
| Corpo do edital → `itens.json` | 391 de 391 palavras preservadas, 0 faltando, 0 alteradas |

- O verticalizado tem 5 disciplinas e 29 tópicos.
- O item 6.1 foi para `observacoes`. A assinatura "FULANO DE TAL" foi para `observacoes_finais`.

**2. Citações**
- A primeira rodada reprovou 6 campos:
  - `Órgão` não tem item numerado no edital.
  - Os 3 mínimos têm percentuais calculados, então passaram a ser derivados.
  - O item 6.1 não está em `itens.json`, então foi citado como `programatico`.
  - As leis foram separadas em um campo por lei, cada um com o seu trecho.
- Depois da correção, todas as citações conferem. Foram 27 campos com citação e 15 `NÃO CONSTA`.

**3. Alertas do edital**

| Alerta | Detalhe |
|---|---|
| Prova já passou | A data provável é 12/10/2026 (item 4.3) e hoje é 23/11/2026. O Painel vai mostrar "Prova já realizada". Passei `--data-prova 2026-10-12`. |
| Quadro do item 4.1 ausente | O item remete a um "quadro a seguir" que não veio na extração (`tabelas.md` vazio). Confira a p. 2 do PDF. |
| Itens por disciplina estimados | Não há quadro, então distribuí os itens de P1 e P2 pelo número de tópicos (28/14/8 e 38/32), confiança baixa. |
| Mínimos (item 5.3) | P1 ≥ 10, P2 ≥ 21 e conjunto ≥ 36 pontos líquidos. Sem branco, isso exige 30, 46 e 78 acertos. O corte do conjunto é o que mais pesa: 10 + 21 = 31, menos que 36. |
| Penalização | +1 por acerto, −1 por erro, 0 em branco (item 5.2). Só marque com mais de 50% de chance de acerto. |
| Cláusula de barreira | A discursiva só é corrigida para quem estiver até a 150ª posição (item 5.4). |
| Marca de teste | O cabeçalho do PDF traz "FICTICIO". |
| Falta no edital | Órgão e nº/data do edital (só no cabeçalho), isenção, duração, desempate, discursiva, validade e bibliografia. |

**4. Suposições do perfil**
- `_perfil-estudos.md` não existe. Usei os padrões do script: 15 h/semana, domínio 0 e incidência 1.
- Assumi que as disciplinas básicas caem em P1 e as específicas em P2 (confiança média).

**5. Custo aproximado**
- Cerca de 20 chamadas de ferramenta em 9 scripts `repl`.
- Quase todas foram `bash` (conferência do ambiente, leitura da skill, extrair, segmentar, cobertura, citações, obsidian). As demais foram escritas de `ficha.json`, `pesos.json` e `analise.md`.
- Não houve `web_fetch` nem busca na web.

**6. Arquivos criados**

Em `/workspace/vault/Concursos/SEFIC-DF 2026 - Teste Agente/`:
- `00 Painel.md`, `01 Ficha.md`, `02 Edital Verticalizado.md`, `03 Edital Integral.md`
- `04 Tabelas (conferir PDF).md`, `05 Análise Estratégica.md`, `99 Relatório de Cobertura.md`
- `Disciplinas/`: `Língua Portuguesa.md`, `Noções de Direito Constitucional.md`, `Legislação.md`, `Infraestrutura.md`, `Banco de Dados.md`
- `_templates/`: `Anotação.md`, `Erro.md`
- Pastas vazias: `Anotações/`, `Questões/`, `Erros/`

Em `/workspace/vault/.concursos-work/sefic-df-2026-teste-agente/` (trabalho intermediário):
- `texto_original.txt`, `texto.txt`, `tabelas.md`, `meta.json`
- `itens.json`, `programatico.txt`, `verticalizado.json`
- `ficha.json`, `pesos.json`, `analise.md`

Não gerei o `Verticalizado.xlsx`, porque é opcional na skill.

**Próximo passo:** confira o quadro do item 4.1 na p. 2 do PDF e, se ele trouxer itens por disciplina, corrija `pesos.json` e as notas de `Disciplinas/`. Depois informe seu domínio de 0 a 5 em cada disciplina e, se houver, uma data de prova atualizada, para eu montar o ciclo.
