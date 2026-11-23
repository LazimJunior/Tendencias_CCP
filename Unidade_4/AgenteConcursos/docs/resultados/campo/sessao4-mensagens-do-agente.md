# Sessão com edital real (SEDES-DF 2026): mensagens

Sessão `sesn_01BD7ESLbVLH7pXUG7HKn7DK`. Texto exato devolvido pela API, sem edição.

## Pedido enviado

Processe o edital real /workspace/vault/_editais/SEDES_2026.pdf para o cargo Técnico em Desenvolvimento e Assistência Social (TDAS), especialidade Técnico Administrativo (cargo 202), do início ao fim, seguindo a skill agente-concursos: extrair, segmentar, ficha com citações validada, cobertura, pesos, análise estratégica e gravação no Obsidian. Use o nome de concurso 'SEDES-DF 2026 - TDAS Técnico Administrativo'. No fim, rode a auditoria do vault e responda com: (1) status: cobertura, citações, auditoria, alertas de injeção e páginas via OCR; (2) as regras que podem eliminar o candidato (mínimos, penalização, cláusula de barreira), cada uma com o item do edital; (3) os 12 campos da ficha que mais pesam na decisão; (4) a lista de arquivos criados no vault.

## Resposta (16:19:59)

Processei o edital completo. A análise usa só o edital original: a banca lista uma retificação (Edital nº 3, de 24/06/2026) que não está em `_editais/` e que não apliquei. O cronograma do edital também já está vencido em relação a hoje (23/11/2026).

## 1. Status

| Verificação | Resultado |
|---|---|
| Cobertura | ✅ 100%. Conteúdo programático: 6.241 de 6.241 palavras. Corpo do edital: 44.318 de 44.318. Nada faltando e nada inventado. |
| Citações | ✅ Todas as 100 conferem. Seis campos ficaram como NÃO CONSTA. |
| Auditoria do vault | ❌ 1 achado, que já existia e não é meu: `_validacao/Teste JS desligado.md`, linha 5, bloco `dataviewjs`. **Não abra essa nota.** Não editei nem apaguei. As notas novas estão limpas. |
| Alertas de injeção | Nenhum. |
| Páginas via OCR | Nenhuma. As 59 páginas tinham texto. |

**Alertas:**
- **Cronograma vencido.** Pelo Anexo I (item 17), a prova do TDAS foi em 06/09/2026, à tarde. A objetiva definitiva saiu em 30/10/2026 (item 23). O resultado preliminar da discursiva é de hoje (item 24). O recurso vai de 24 a 30/11/2026 (item 26). Gerei o Painel sem data de prova.
- **Retificação não aplicada.** Para aplicar, coloque o PDF em `_editais/` e peça a retificação com o texto exato.
- **Distribuição de questões estimada (confiança baixa).** O edital só dá o total por área, 20 de gerais e 40 de específicos (item 11.1). Distribuí pelo número de tópicos. Está marcado como estimado.
- **Perfil ausente.** Não existe `_perfil-estudos.md`. Usei 15 h/semana e domínio 0 como padrão.
- **Erros materiais do edital, mantidos literais:**
  - Existe um item numerado só "4.", depois do 4.3.
  - O número 15.7 aparece duas vezes.
  - O Anexo I, itens 38, 40 e 41, está com ano 2026, enquanto os itens 30 a 39 estão em 2027.
  - O conteúdo do Agente Social traz "10.4" no lugar de 5.4.
- **Skill sumiu no meio da sessão.** `/workspace/skills/agente-concursos/` ficou vazio. Terminei com a cópia em `/workspace/vault/.agente-setup/agente-concursos/`. Ela é uma versão mais nova e gera o Painel sem JavaScript por padrão. Vale checar por que a pasta esvaziou.
- **Verticalizado com todos os cargos.** Ele contém os conteúdos dos outros cargos, para manter a integralidade. Só estude os blocos do TDAS que o cargo 202 usa: 20.2.2.1, 20.2.2.2, 20.2.3.1.1, 20.2.3.1.2 e 20.2.3.2.3.

## 2. Regras que podem eliminar

| Regra | Item | Em acertos |
|---|---|---|
| **Penalização:** não há. Errada, em branco ou dupla vale 0,00. Nunca deixe em branco. | 12.4.2 c | — |
| **Mínimo em Conhecimentos Gerais:** nota inferior a 10,00 elimina. | 12.4.4 a | 10 de 20 acertos |
| **Mínimo em Conhecimentos Específicos:** nota inferior a 40,00 elimina. | 12.4.4 b | 20 de 40 acertos (2 pontos cada) |
| **Cláusula de barreira:** só corrigem a discursiva dos 4.776 melhores do Técnico Administrativo (AC 2.388, PCD 957, PPP 954, HIPO 477), respeitados os empates na última posição. | 12.4.4 c, 12.4.5, 12.4.5.1 | Corte por classificação, sem nota mínima |
| **Discursiva não corrigida:** eliminação automática. | 13.3.2 | — |
| **Mínimo na discursiva:** abaixo de 50,00 elimina. | 13.3.7 | Ver análise abaixo |
| **Nota zero na discursiva:** fuga ao tema, lápis, tinta fora do padrão, menos de 20 linhas, marca identificadora e outros casos. | 13.3.4.5, 13.2.5 | — |
| **Certidão negativa de ações criminais fora do prazo ou com condenação por violência doméstica.** | 16.6.1.3 | — |
| **Declaração falsa na inscrição.** | 9.6.1.3 | — |
| **Documento de identidade original inválido** (cópia não vale). | 19.9, 19.10 a | — |
| **Ficar menos de 2 horas na sala.** | 19.14 | — |
| **Ausência ou atraso:** não há segunda chamada. | 19.13, 19.19 | — |
| **Objetos vedados:** celular, relógio, fone, wearable, lápis, borracha, marca-texto, chapéu, garrafa não transparente. | 19.21 | — |
| **Eletrônico fora da embalagem lacrada, ou que ligue durante a prova.** | 19.21.5, 19.21.5.1 | — |
| **Cola, auxílio, sair sem fiscal, levar a folha de respostas.** | 19.23 | — |
| **Tempo adicional deferido a quem não for considerado PCD na avaliação biopsicossocial.** | 10.6.1 | — |

**Análise da discursiva (derivada da fórmula do item 13.3.4.4, confiança média):**
- Cada ponto de CAC (conteúdo e atendimento ao comando) vale 23,33. Cada ponto de OT ou DLP vale 5,00.
- Com CAC 3, passa sempre (70,00).
- Com CAC 2, precisa de pelo menos 1 ponto em OT ou DLP (51,67).
- Com CAC 1, só passa com OT 3 e DLP 3 (53,33).
- Com CAC 0, não passa (máximo 30,00).
- Parto da premissa de que as notas são inteiras de 0 a 3, porque os itens 13.3.4.1.1, 13.3.4.2.1 e 13.3.4.3.1 só descrevem esses quatro níveis.

**Barreira em contexto (dado externo, confiança média-baixa):** notícias de agosto/2026 citam cerca de 98,4 mil inscrições homologadas para Técnico Administrativo. As fontes divergem em 5 candidatos. Seriam cerca de 4,9% dos inscritos corrigidos. O edital não informa esse número.

## 3. Os 12 campos que mais pesam

| # | Campo | Valor | Item |
|---|---|---|---|
| 1 | Estrutura da objetiva | 20 gerais × 1 + 40 específicos × 2 = 100 pontos, 5 alternativas | 11.1, 12.2 |
| 2 | Penalização | Nenhuma (erro = 0) | 12.4.2 c |
| 3 | Mínimos | 10 pontos em gerais e 40 em específicos | 12.4.4 |
| 4 | Barreira | 4.776 corrigidos | 12.4.5.1 |
| 5 | Discursiva | Redação de 20 a 30 linhas, 100 pontos, mínimo 50 | 13.1, 13.3.7 |
| 6 | Vagas (cargo 202) | 398 imediatas (AC 198) + 1.194 cadastro de reserva = 1.592 | 4.1.1 |
| 7 | Remuneração | R$ 4.320,16 + vale-alimentação de R$ 640,00, 30 horas semanais | 2.3.4 a 2.3.6 |
| 8 | Prova | 06/09/2026, tarde, 4 horas | Anexo I item 17, 11.3 |
| 9 | Taxa e inscrição | R$ 84,00, de 09/06 a 13/07/2026 | 9.1, Anexo I item 8 |
| 10 | Requisito | Ensino médio ou médio técnico | 2.3.3 |
| 11 | Data de corte da legislação | Publicação do edital (14/05/2026 no Anexo I; edital datado de 13/05/2026) | 19.31.2 |
| 12 | Lei Maria da Penha | No mínimo 3 questões na objetiva | 20.2.2.2 (nota *) |

Os pesos estimados e as demais regras estão em `05 Análise Estratégica.md`. O específico do cargo 202 concentra 54% dos pontos da objetiva (27 questões estimadas, ou 3,18 pontos por tópico).

## 4. Arquivos no vault

Pasta `/workspace/vault/Concursos/SEDES-DF 2026 - TDAS Técnico Administrativo/`, com 35 arquivos:
- `00 Painel.md`
- `01 Ficha.md`
- `02 Edital Verticalizado.md`
- `03 Edital Integral.md`
- `04 Tabelas (conferir PDF).md`
- `05 Análise Estratégica.md`
- `99 Relatório de Cobertura.md`
- `Verticalizado.xlsx`
- `Disciplinas/`, com 25 notas
- `_templates/Anotação.md` e `_templates/Erro.md`
- `Anotações/`, `Questões/` e `Erros/`, vazias

Trabalho intermediário em `/workspace/vault/.concursos-work/sedes-df-2026-tdas-tecnico-administrativo/`: `texto.txt`, `itens.json`, `verticalizado.json`, `ficha.json`, `pesos.json`, `analise.md` e outros.

**Próximo passo:** coloque o PDF da retificação (Edital nº 3, de 24/06/2026) em `_editais/` para eu aplicar e refazer a verticalização e a ficha. Em seguida, me passe horas por semana e domínio por disciplina para eu montar o ciclo.
