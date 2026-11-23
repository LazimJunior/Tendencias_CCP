---
marp: true
theme: gaia
class: invert
paginate: true
style: |
  section { font-size: 24px; }
  table { font-size: 19px; }
---

<!-- _paginate: false -->

# Agente de Estudos para Concursos
### Do edital em PDF ao plano de estudos no Obsidian, sem perder uma linha

Tendências em Ciência da Computação · Unidade IV, Agentes e Ética · UDF 2026/2

---

## O problema

- O edital define **tudo**: disciplinas, pesos, penalização, mínimos e a lista exata de tópicos
- Verticalizar à mão leva horas. **Um tópico pulado só aparece na prova**
- Pedir a um chatbot é rápido, mas listas longas viram "*… e demais tópicos*"
- Retificações mudam o edital no meio do estudo

**Objetivo:** um agente que organiza o edital com IA e **prova por código** que nada foi perdido ou inventado.

---

## Prompt direto × agente

| | Chat comum | Agente de Concursos |
|---|---|---|
| Conteúdo programático | pode ser resumido | **literal + cobertura 100%** |
| Origem dos dados | não informada | item e página do edital |
| Regras da banca | "memória" do modelo | só do edital ("NÃO CONSTA") |
| Retificação | refazer tudo | diff + confirmação |
| PDF malicioso | pode obedecer | detectado e tratado como dado |
| Progresso | fora da conversa | checklist no Obsidian, preservado |

---

## Arquitetura: 4 camadas

| Camada | Quem faz | O quê |
|---|---|---|
| **1. Perceptiva** | script | PDF → texto, OCR, cabeçalhos, **anti-injeção**, segmentação |
| **2. Cognitiva** | Claude + skill | estrutura, ficha com trechos literais, análise, anotações |
| **3. Decisória** | script | **cobertura**, **citações**, numeração, prioridade, proteção do progresso |
| **4. Executiva** | script + worker | grava no vault: Painel, Ficha, Verticalizado, Disciplinas |

**Princípio:** o modelo interpreta, o código confere.
Claude Console (Managed Agents) + worker no WSL + vault do Obsidian.

---

## Como a fidelidade é garantida

- **Cobertura:** compara o edital com o verticalizado **palavra por palavra, nos dois sentidos**
  - faltou → `FALTANDO` · inventou ou duplicou → `NÃO CONFERE` · só mudou de lugar → aviso
- **Citações:** cada campo da ficha precisa do item, do trecho literal e dos mesmos números
- **Retificação:** só aplica se o trecho casar exatamente 1 vez; `comparar` mostra o que mudou
- **Progresso:** nada é sobrescrito, a atualização vai para `_atualizacao-<data>/`

---

## Ética, privacidade e vieses

- **LGPD:** dados só do titular, no computador dele. Listas de candidatos (dados de terceiros) ficam **fora**
- **Segurança:** WSL sem acesso ao C: nem ao Windows. Chave de API fora do alcance do agente. Teto de gasto por sessão
- **Prompt injection:** PDF com "ignore as instruções…" é sinalizado e **não obedecido**
- **Vieses:** regras da banca só do edital, estimativas marcadas, incidência neutra sem dado real, questões rotuladas como inéditas
- **Transparência:** item e página em cada dado, relatório de cobertura no vault

---

## Testes

| Cenário | Resultado |
|---|---|
| Edital numerado / sem numeração | ✅ cobertura 100% |
| IA omite, inventa, resume ou duplica | ✅ reprovado |
| Citação errada na ficha | ✅ reprovada |
| Retificação / reexecução | ✅ aplicada 1 vez, rastreável |
| Prompt injection no PDF | ✅ sinalizado, texto preservado |
| Progresso marcado + reexportação | ✅ nenhum `[x]` perdido |

**31/31 casos passando** · teste de mutação: **6/6 defeitos detectados**
Achado real: ligadura "ﬁ" do PDF quebrava citações corretas (corrigido)

---

## Conclusão

**Vantagens:** fidelidade comprovável · estudo num lugar só · custo baixo (US$ 0,27 medido no edital de teste; ~US$ 1 estimado por edital real)
**Limitações:** validado só com edital fictício (Managed Agents em beta) · tabelas/OCR exigem conferência · heurísticas · nota com `dataviewjs` roda no Windows (risco confirmado no teste)

**Próximos passos:** incidência real por tópico · avaliação automática da ficha (*evals*) · checagem semanal de retificações

> IA confiável não é a que acerta sempre: é a que **prova** quando acertou.
