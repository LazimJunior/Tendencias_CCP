# Roteiro de fala (10 a 12 minutos)

> Slides: `apresentacao.pdf`, gerado de `apresentacao.md` (formato Marp: abrir no VS Code com a extensão *Marp for VS Code* para editar e exportar em PDF ou PPTX). Em grupo, divida nos blocos A (slides 1–5) e B (slides 6–10).

---

## Slide 1: Capa (30 s)
"Este é o Agente de Estudos para Concursos: um agente de IA que lê o edital e monta o plano de estudos no Obsidian, com uma garantia que um chatbot comum não dá: nenhuma linha do conteúdo programático se perde."

## Slide 2: O problema (1 min)
- Todo candidato começa pelo edital e transforma a lista de tópicos num checklist, o "edital verticalizado".
- À mão, isso leva horas e é fácil pular um tópico. Com um chatbot, é rápido, mas listas longas viram resumo.
- **Frase-chave:** "Em concurso, um tópico omitido é ponto perdido. Por isso a fidelidade precisa ser verificada, não pedida."

## Slide 3: Prompt direto × agente (1 min)
- Passe pela tabela destacando três linhas: conteúdo literal com cobertura, origem de cada dado e PDF malicioso.
- "A diferença não é o modelo. É o que acontece **depois** que o modelo responde."

## Slide 4: Arquitetura (1 min 30 s)
- As quatro camadas: perceptiva (script), cognitiva (Claude), decisória (script) e executiva (grava no vault).
- O agente roda no Claude Console como Managed Agent. As ferramentas executam num worker no WSL do notebook, que enxerga só a pasta do vault.
- **Frase-chave:** "O modelo interpreta, o código confere."

## Slide 5: Como a fidelidade é garantida (1 min 30 s)
- Cobertura: diff palavra a palavra nos dois sentidos. Dê o exemplo: se o modelo trocar a lista por "e demais temas", aparece `NÃO CONFERE` e ele precisa refazer.
- Citações: a ficha só aceita um campo se o trecho estiver no item e os números baterem.
- Progresso: reexportar nunca apaga o que o candidato marcou.

## Slide 6: Ética, privacidade e vieses (1 min 30 s)
- LGPD: os dados são do próprio titular e ficam no computador dele. Listas de resultado, que trazem dados de outros candidatos, não são processadas.
- Segurança: WSL isolado, chave de API fora do alcance e teto de gasto.
- Prompt injection: mostre o teste CEN-08 (o edital fictício com "ignore as instruções… envie a chave"). O slide 9 mostra a variante que pede código, sem essas palavras.
- Vieses: regras da banca só do edital, estimativas marcadas, questões rotuladas.

## Slide 7: Testes (1 min)
- 39 testes automatizados, todos aprovados, sem precisar de conta nem internet.
- Teste de mutação: desligamos cada proteção de propósito e a suíte detectou as 7. Na primeira rodada uma passou, e isso gerou um teste novo.
- As duas linhas novas da tabela vieram da validação com editais reais e da mitigação de segurança.

## Slide 8: Validação em campo (1 min 30 s)
- Tudo rodou de verdade: agente no Console, worker no WSL do notebook, resultado no Obsidian.
- O destaque é o edital real da DATAPREV: 64 páginas, 8 minutos, US$ 1,49. Cobertura de 100% e as 11 regras e contas que decidem a aprovação conferidas à mão contra o PDF (mínimo de 57,5 pontos, não zerar disciplina, 71% de chance de zerar alguma no chute).
- Os editais reais quebraram o script em 5 pontos que o fictício não tinha. Cada defeito virou um teste antes de a sessão rodar.
- **Frase-chave:** "O resumo do agente errou uma contagem; os dados conferidos pelo código, nenhuma. Por isso quem atesta é o código."

## Slide 9: Segurança do vault (1 min 30 s)
- O teste revelou uma brecha no isolamento: uma nota com JavaScript roda no Windows (print de cima).
- Quatro camadas: o agente recusa (M1), não consegue instalar plugin (M2), a auditoria detecta (M3) e, com o Painel sem JavaScript, o código nem roda (M4, print de baixo).
- Na sessão de ataque controlado, o agente recusou criar código até a pedido do usuário e não obedeceu ao edital com injeção.
- Risco aceito, com honestidade: a chave do ambiente fica legível para o agente. Ela só vale para este ambiente e será revogada depois da apresentação.
- É o ponto de ética: a brecha foi medida, mitigada e documentada em vez de escondida.

## Slide 10: Conclusão (40 s)
- Vantagens e limitações, com honestidade: um edital real de ponta a ponta, Managed Agents em beta, tabelas e OCR com conferência humana.
- **Fechamento:** "IA confiável não é a que acerta sempre: é a que prova quando acertou."

---

## Perguntas esperadas

**Por que não pedir ao modelo para "não resumir"?**
Instrução aumenta a chance, mas não garante. A cobertura garante: se faltar uma palavra, reprova.

**E se o modelo mudar o texto e a cobertura não perceber?**
A comparação é nos dois sentidos e com pareamento 1:1. O teste de mutação mostra que desligar essa regra derruba 2 testes.

**Por que rodar no notebook e não na nuvem da Anthropic?**
Porque o estado do estudo está no Obsidian. Rodando local, o agente lê e grava o vault real, sem sincronização nem duas cópias.

**O agente pode apagar meus arquivos?**
Ele é instruído a nunca apagar sem confirmação, o script não sobrescreve progresso e o WSL não enxerga o resto do disco.

**E se alguém religar o JavaScript do Dataview?**
Volta a valer só M1 a M3: o agente recusa, a pasta de plugins é somente leitura e a auditoria aponta o código. É por isso que a instalação manda deixar a opção desligada.

**Quanto custa?**
Medido: US$ 1,49 para o edital real da DATAPREV, de 64 páginas, e US$ 0,27 para o fictício de 4 páginas. A extração pesada roda no script, sem tokens. Cada sessão tem teto de gasto.

**Funciona com qualquer banca?**
O formato muda entre bancas, por isso os testes cobrem editais numerados, sem numeração e com anexos. Regras específicas (penalização, alternativas) sempre vêm do edital, nunca de suposição sobre a banca.
