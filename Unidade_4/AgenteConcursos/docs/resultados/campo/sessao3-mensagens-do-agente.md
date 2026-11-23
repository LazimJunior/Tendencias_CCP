# Sessão com edital real (DATAPREV 2026): mensagens

Sessão `sesn_01X6vMyS442kG2RS17V6Tp7u`. Texto exato devolvido pela API, sem edição.

## Pedido enviado

Processe o edital real /workspace/vault/_editais/DATAPREV_2026.pdf para o cargo Analista de Tecnologia da Informação, Perfil 3: Desenvolvimento de Software, do início ao fim, seguindo a skill agente-concursos: extrair, segmentar, ficha com citações validada, cobertura, pesos, análise estratégica e gravação no Obsidian. Use o nome de concurso 'DATAPREV 2026 - Analista TI Perfil 3'. No fim, rode a auditoria do vault e responda com: (1) status: cobertura, citações, auditoria, alertas de injeção e páginas via OCR; (2) as regras que podem eliminar o candidato (mínimos, penalização, cláusula de barreira), cada uma com o item do edital; (3) os 12 campos da ficha que mais pesam na decisão; (4) a lista de arquivos criados no vault.

## Resposta (15:48:54)

# DATAPREV 2026 – Analista de TI, Perfil 3: processamento concluído

## 1) Status

| Verificação | Resultado |
|---|---|
| Cobertura | ✅ 100%. Nada removido e nada inventado, tanto no conteúdo programático quanto no corpo do edital. Há 1 aviso "MOVIDO" (sem perda), explicado abaixo. |
| Citações | ✅ Todas conferem (69 campos validados). 6 campos ficaram como NÃO CONSTA. |
| Auditoria do vault | ✅ Nenhum código fora do Painel, em 49 notas. |
| Alertas de injeção | Nenhum. Também busquei por termos suspeitos no texto inteiro e não achei nada. |
| Páginas via OCR | Nenhuma. As 64 páginas tinham texto. |

Alertas que mudam a leitura do material:
- **Datas já passadas.** O edital marca inscrições até 06/08/2026 (item 4.1) e prova em 11/10/2026 (item 9.1). A sessão é de 23/11/2026. Não há retificação no vault. Confira no site da FGV se houve adiamento ou novo edital.
- **Só Módulo I e Perfil 3 ficam estruturados.** O verticalizado só estrutura o Módulo I e o Perfil 3. Os textos dos outros 12 perfis foram para "Texto final do anexo" em `02 Edital Verticalizado`, literais. Foi assim para o Painel não listar umas 90 disciplinas que não são suas. O aviso "MOVIDO" da cobertura é esse reagrupamento.
- **"TESTES" no meio da numeração.** O edital põe o cabeçalho "TESTES" no meio da numeração de Desenvolvimento de Sistemas. Os itens 7.1 a 20 (RPA, ágeis, ponto de função, front-end, blockchain, microsserviços) ficaram sob esse cabeçalho, na ordem original. Pela numeração, são continuação de Desenvolvimento de Sistemas (confiança média). Estude os dois como um bloco só.
- **Questões do Módulo II estimadas.** O edital só dá 30 questões de peso 2,5 para todo o Módulo II (item 9.5). A divisão entre os 6 blocos do perfil é estimada pelo número de tópicos, com confiança baixa. Desenvolvimento + Testes ficam com cerca de 15 questões, BD com 6.
- **Horas e domínio assumidos.** Sem `_perfil-estudos.md`, assumi 15 h/semana no Painel e domínio 0 em tudo. Ajuste os dois.
- **Quadro de vagas conferido.** O quadro do item 3.1 foi conferido pelas coordenadas do PDF (p. 2). O Perfil 3 ocupa as 7 linhas entre o Perfil 2 e o Perfil 4.

## 2) Regras que podem eliminar

| Regra | Efeito | Item |
|---|---|---|
| Mínimo de **57,5 pontos** (50% de 115) | Eliminação | 9.17 a, 9.18 |
| **Não zerar nenhuma disciplina** (5 do Módulo I + Conhecimentos Específicos) | Eliminação | 9.17 b, 9.18 |
| Corte por classificação: fora do nº de vagas do cadastro de reserva do seu perfil e localidade | Eliminação | 14.4, 3.1, 11.5 |
| Comprovação dos requisitos do Anexo II na contratação | Eliminação | ANEXO VII 1 e 1.1, 3.5 |
| Exame médico admissional (recurso em até 3 dias úteis) | Eliminação | ANEXO VII 10 a 13 |
| Portões fecham às 12h30 | Eliminação | 9.3, 10.1.1, 10.14 p |
| Faltar à prova (não há segunda chamada) | Eliminação | 9.4, 10.11 |
| Documento original com foto (cópia não vale) | Eliminação | 10.3 |
| Sair antes de 2 h de prova | Prova não corrigida e eliminação | 10.7, 10.7.1 |
| Relógio, celular, lápis, lapiseira, borracha, corretivo, boné, óculos escuros | Eliminação | 10.13, 10.14 c |
| Não entregar o cartão de respostas | Eliminação | 9.14 |
| Recusar o detector de metais ou a impressão digital | Eliminação | 10.14 n, o |
| Erro grosseiro no nome ou documento que não conste no cadastro | Eliminação | 4.11.1 |

- **Penalização por erro:** não há no edital (confiança alta). Só vale nota zero para questão com mais de uma marcação, em branco, emenda ou rasura (9.9). Chutar rende +0,20 ponto por questão no Módulo I e +0,50 no Módulo II. Nunca deixe em branco.
- **Cláusula de barreira:** NÃO CONSTA. A prova é única e objetiva, sem discursiva (2.1).
- **Mínimo em acertos:**
  - Com 40/40 no Módulo I, ainda precisa de 7/30 no Módulo II.
  - Com 28/40, precisa de 12/30.
  - Com 20/40, precisa de 15/30.
  - Só com o Módulo I não se passa.
- **Risco de zerar:** chutando tudo, a chance de zerar ao menos uma disciplina é 71%. Raciocínio Lógico e Legislação (5 questões cada) têm 32,8% de zerar sozinhas. Garantir 1 acerto em cada é barato.
- **Corte por localidade** (confiança média, porque o edital não diz se o 14.4 conta por lista ou pelo total):
  - Fortaleza, João Pessoa, Natal e Florianópolis: 100 vagas cada (20 imediatas + 80 de cadastro). Na ampla concorrência são 65.
  - Brasília, Rio de Janeiro e São Paulo: só cadastro de reserva, 17 cada. Na ampla concorrência são 11.

## 3) Os 12 campos que mais pesam

| # | Campo | Valor | Item |
|---|---|---|---|
| 1 | Mínimo | ≥ 57,5 pts e não zerar disciplina | 9.17 |
| 2 | Estrutura | 70 questões, 5 alternativas. Módulo I: 40 questões de peso 1. Módulo II: 30 questões de peso 2,5. Total 115 | 9.5, 9.6 |
| 3 | Penalização | Nenhuma por erro | 9.9 |
| 4 | Cláusula de barreira | NÃO CONSTA (etapa única) | 2.1 |
| 5 | Vagas do Perfil 3 | 80 imediatas (4 capitais) + 17 de cadastro em cada uma das outras 3 | 3.1 |
| 6 | Corte por classificação | Eliminado quem ficar fora do nº de vagas do cadastro de reserva | 14.4 |
| 7 | Prova | 11/10/2026, 13h–17h; portões às 12h30 | 9.1, 9.3 |
| 8 | Remuneração | R$ 10.685,44 (R$ 9.423,30 + R$ 1.262,14), 40 h, CLT | ANEXO III, 3.6 |
| 9 | Requisito | Graduação em TI, ou qualquer graduação + pós em TI de 360 h | ANEXO II |
| 10 | Desempate | 60+ anos → maior nota em Específicos → Português → Inglês → jurado → mais velho | 12.1 |
| 11 | Data de corte da legislação | NÃO CONSTA | — |
| 12 | Validade | 2 anos, prorrogável; começa depois de 14/01/2027 | 1.2, 15.5.1 |

Também NÃO CONSTAM: código do cargo, datas de gabarito e resultado, bibliografia, e etapas de títulos, TAF, psicológica e curso de formação.

## 4) Arquivos criados

Pasta `/workspace/vault/Concursos/DATAPREV 2026 - Analista TI Perfil 3/`:
- `00 Painel.md`
- `01 Ficha.md`
- `02 Edital Verticalizado.md`
- `03 Edital Integral.md`
- `04 Tabelas (conferir PDF).md`
- `05 Análise Estratégica.md`
- `99 Relatório de Cobertura.md`
- `Disciplinas/`, com 11 notas: Língua Portuguesa, Língua Inglesa, Raciocínio Lógico, Atualidades e Inteligência Artificial, Legislação, Desenvolvimento de Sistemas, Testes, Inteligência de Negócios, Segurança da Informação, Banco de Dados, Gestão e Governança de TI.
- `Anotações/`, `Questões/` e `Erros/` (vazias).
- `_templates/Anotação.md` e `_templates/Erro.md`.

Trabalho intermediário em `/workspace/vault/.concursos-work/dataprev-2026-analista-ti-perfil-3/`:
- `texto.txt` (e `texto_original.txt`)
- `itens.json`
- `verticalizado.json`
- `verticalizado_segmentacao_automatica.json` (saída original do segmentador, antes do ajuste de estrutura)
- `ficha.json`
- `pesos.json`
- `analise.md`
- `cobertura.md` e `citacoes.md`
- `tabelas.md` e `meta.json`
- `restruturar.py` e `analise_gerar.py`, scripts que reproduzem o ajuste de estrutura e a análise.

Não gerei o `Verticalizado.xlsx` (opcional na skill) nem o ciclo de estudos, porque não foram pedidos.

**Próximo passo:** me diga suas horas por semana e seu domínio de 0 a 5 em cada disciplina, e confirme com a FGV o status das datas. Com isso monto o ciclo de estudos e corrijo o Painel.
