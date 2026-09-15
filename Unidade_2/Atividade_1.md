# Programação Assistida e Automação com IA

## Identificação

- **Nome:** Lazim Francisco de Oliveira Junior
- **Turma:** Tendências em Ciência da Computação — 8º semestre — UDF
- **Data:** 15/09/2026
- **Ferramenta de IA utilizada:** Claude (Anthropic)
- **Problema escolhido:** Opção A — Organização de Arquivos

---

## 1. Problema

Preciso organizar automaticamente os arquivos soltos dentro de uma pasta, agrupando-os em subpastas de acordo com a extensão (PDF, JPG, XLSX, TXT, ZIP, PY etc.), de forma parecida com o exemplo de padronização de relatórios apresentado no material da aula (pasta `trabalhos/` com nomes inconsistentes).

Esse é um problema real e recorrente no meu dia a dia: na Bloom BR eu lido constantemente com pastas de exportações (relatórios do Shopify, planilhas do Omie, comprovantes, imagens de produto) que chegam misturadas e precisam ser separadas antes de qualquer processamento.

## 2. Entrada

- O caminho de uma pasta local contendo arquivos diversos, com extensões variadas.
- Alguns arquivos podem não ter extensão (ex.: `README`, `LICENSE`).
- A pasta pode conter subpastas (que não devem ser reorganizadas).
- A pasta pode não existir ou estar vazia.

## 3. Processamento

Para cada arquivo dentro da pasta informada:

1. identificar a extensão do arquivo (ou marcá-lo como "sem extensão");
2. determinar a subpasta de destino correspondente à extensão;
3. criar a subpasta de destino caso ainda não exista;
4. mover o arquivo para a subpasta, sem sobrescrever arquivos já existentes com o mesmo nome;
5. registrar (log) cada operação realizada;
6. tratar erros sem interromper a execução (pasta inexistente, falha de permissão etc.).

## 4. Saída Esperada

- Pasta organizada em subpastas nomeadas pela extensão em maiúsculas (`PDF/`, `JPG/`, `XLSX/`, `TXT/`, `ZIP/`, `PY/`), e uma subpasta `SEM_EXTENSAO/` para arquivos sem extensão.
- Nenhum arquivo original excluído.
- Nenhum arquivo sobrescrito em caso de nomes repetidos (renomeação automática com sufixo numérico).
- Um resumo final informando quantos arquivos foram movidos, ignorados e quantos erros ocorreram.

## 5. Prompt Utilizado

Prompt estruturado, seguindo o modelo indicado no material (PAPEL + PROBLEMA + ENTRADA + SAÍDA + TECNOLOGIA + RESTRIÇÕES + CASOS DE TESTE + CRITÉRIOS DE QUALIDADE):

```
Atue como desenvolvedor Python.

PROBLEMA:
Preciso organizar automaticamente os arquivos soltos dentro de uma pasta,
agrupando-os em subpastas de acordo com a extensão.

ENTRADA:
Caminho de uma pasta local contendo arquivos de extensões variadas.

SAÍDA ESPERADA:
A mesma pasta, com os arquivos movidos para subpastas nomeadas
pela extensão (ex.: PDF, JPG, TXT).

LINGUAGEM:
Python 3, utilizando apenas a biblioteca padrão.

RESTRIÇÕES:
- não excluir nenhum arquivo;
- não sobrescrever arquivos existentes;
- não reorganizar subpastas já existentes.

FORMATO:
1. explique a estratégia;
2. apresente o código;
3. explique as principais linhas;
4. apresente um exemplo de execução.
```

## 6. Código Inicial

Primeira versão gerada com apoio da IA a partir do prompt acima:

```python
import os
import shutil

def organizar_arquivos(pasta):
    arquivos = os.listdir(pasta)

    for nome in arquivos:
        caminho = os.path.join(pasta, nome)

        if os.path.isfile(caminho):
            extensao = nome.split(".")[-1].upper()
            pasta_destino = os.path.join(pasta, extensao)

            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)

            shutil.move(caminho, os.path.join(pasta_destino, nome))

    print("Arquivos organizados com sucesso!")

organizar_arquivos("minha_pasta")
```

## 7. Análise Crítica (antes de executar)

Usando o checklist da Etapa 3 do material, identifiquei os seguintes problemas **antes** de rodar o código em um caso real:

| Verificação | Resultado |
|---|---|
| Eu compreendo o código? | Sim, é direto. |
| Atende ao problema definido? | Parcialmente. |
| Há bibliotecas que não conheço? | Não, apenas `os` e `shutil` (padrão). |
| Há operações que podem apagar ou sobrescrever dados? | **Sim — risco real.** `shutil.move` sobrescreve o destino silenciosamente se o arquivo já existir lá. |
| O código utiliza dados sensíveis? | Não. |
| Há tratamento de erros? | **Não.** Se a pasta não existir, o programa quebra com `FileNotFoundError`. |
| Existem casos que o código não considera? | **Sim.** Arquivos sem extensão (`nome.split(".")[-1]` retorna o próprio nome do arquivo quando não há ponto), o que gera colisão entre o nome do arquivo e o nome da pasta de destino. |
| O caminho da pasta está fixo (`"minha_pasta"`) | Sim — não é reutilizável, precisa virar parâmetro/CLI. |

Essa análise foi confirmada na prática pelos testes da próxima seção — os dois riscos mais graves (arquivo sem extensão e sobrescrita) realmente quebraram o programa.

## 8. Casos de Teste

Executei a versão inicial em três cenários, com pastas de teste reais.

### Teste 1 — Caso normal

```
Entrada: pasta com 7 arquivos (pdf, PDF, jpg, xlsx, txt, zip, py)
→ resultado esperado: cada arquivo movido para a subpasta da sua extensão
```

**Resultado:** ✅ passou.

```
t1/JPG/foto_evento.jpg
t1/PDF/Relatorio João FINAL.pdf
t1/PDF/relatorio_maria.PDF
t1/PY/script.py
t1/TXT/notas.txt
t1/XLSX/planilha_vendas.xlsx
t1/ZIP/backup.zip
```

### Teste 2 — Caso limite (arquivo sem extensão)

```
Entrada: pasta com "README" e "LICENSE" (sem extensão)
→ comportamento esperado: os arquivos deveriam ir para alguma
   subpasta de "sem extensão", sem erro
```

**Resultado:** ❌ **falhou** — o programa quebrou com o traceback abaixo:

```
NotADirectoryError: [Errno 20] Not a directory: 'teste2/LICENSE/LICENSE'
```

**Causa raiz:** `nome.split(".")[-1]` retorna o próprio nome do arquivo quando não há `.` (ex.: `"LICENSE"` → `"LICENSE"`). O script então tenta criar uma pasta chamada `LICENSE` — mas já existe um **arquivo** com esse mesmo nome no mesmo diretório —, e a chamada `shutil.move` falha ao tentar mover o arquivo para dentro de si mesmo.

### Teste 3 — Caso de erro (pasta inexistente)

```
Entrada: "pasta_que_nao_existe"
→ comportamento esperado: mensagem de erro amigável, sem travar
```

**Resultado:** ❌ **falhou** — o programa encerrou com traceback não tratado:

```
FileNotFoundError: [Errno 2] No such file or directory: 'pasta_que_nao_existe'
```

## 9. Problemas Encontrados (resumo)

1. Sem tratamento de erro para pasta inexistente (crash com traceback cru).
2. Sem tratamento para arquivos sem extensão (crash por colisão de nome arquivo/pasta).
3. Risco de sobrescrita silenciosa quando já existe um arquivo com o mesmo nome na pasta de destino.
4. Caminho da pasta fixo no código (`"minha_pasta"`), sem parametrização via CLI.
5. Uso de `print` em vez de log estruturado — difícil auditar o que foi feito.
6. Sem `if __name__ == "__main__":` — qualquer `import` do módulo já dispara a execução.
7. Sem resumo quantitativo da execução (quantos arquivos movidos/ignorados/com erro).

## 10. Prompt de Refatoração

```
Revise o código abaixo.

O programa já funciona para o caso normal, mas os testes mostraram falhas:
- quebra com FileNotFoundError se a pasta não existir;
- quebra com NotADirectoryError para arquivos sem extensão (ex.: "LICENSE"),
  porque cria uma pasta com o mesmo nome do arquivo;
- sobrescreve silenciosamente arquivos de mesmo nome no destino.

Agora analise e corrija considerando:
- clareza;
- organização;
- duplicação;
- nomes de variáveis e funções;
- tratamento de erros;
- adicionar modo --dry-run (simulação sem mover arquivos de fato);
- não sobrescrever arquivos (renomear em caso de conflito);
- tratar arquivos sem extensão numa pasta "SEM_EXTENSAO";
- usar type hints, docstrings e logging em vez de print.

Não altere o comportamento esperado para o caso normal (Teste 1).
Explique cada alteração proposta.

[CÓDIGO]
```

## 11. Código Refatorado

```python
"""
Script de automação: organiza arquivos de uma pasta em subpastas por extensão.

Uso:
    python organiza_arquivos_v2.py <pasta> [--dry-run]

Requisitos atendidos:
- não exclui nenhum arquivo;
- não sobrescreve arquivos existentes (renomeia em caso de conflito);
- trata arquivos sem extensão (vão para a subpasta SEM_EXTENSAO);
- trata pasta inexistente sem travar o programa;
- permite simulação (--dry-run) antes de mover de fato.
"""

import argparse
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

SEM_EXTENSAO = "SEM_EXTENSAO"


def obter_extensao(nome_arquivo: str) -> str:
    """Retorna a extensão do arquivo em maiúsculas, ou 'SEM_EXTENSAO' se não houver."""
    sufixo = Path(nome_arquivo).suffix  # ex.: '.pdf' ou '' se não houver ponto
    if not sufixo:
        return SEM_EXTENSAO
    return sufixo[1:].upper()


def destino_sem_conflito(pasta_destino: Path, nome_arquivo: str) -> Path:
    """Gera um caminho de destino que não sobrescreve um arquivo já existente."""
    caminho = pasta_destino / nome_arquivo
    if not caminho.exists():
        return caminho

    base = Path(nome_arquivo).stem
    extensao = Path(nome_arquivo).suffix
    contador = 1
    while True:
        candidato = pasta_destino / f"{base}_{contador}{extensao}"
        if not candidato.exists():
            return candidato
        contador += 1


def organizar_arquivos(pasta: str, dry_run: bool = False) -> dict:
    """
    Organiza os arquivos de `pasta` em subpastas nomeadas pela extensão.

    Parâmetros:
        pasta (str): caminho da pasta a organizar.
        dry_run (bool): se True, apenas simula e não move nenhum arquivo.

    Retorna:
        dict com o resumo da execução: {"movidos": int, "ignorados": int, "erros": list}
    """
    caminho_pasta = Path(pasta)
    resumo = {"movidos": 0, "ignorados": 0, "erros": []}

    if not caminho_pasta.exists():
        logger.error("Erro: a pasta '%s' não existe.", pasta)
        resumo["erros"].append(f"Pasta inexistente: {pasta}")
        return resumo

    if not caminho_pasta.is_dir():
        logger.error("Erro: '%s' não é uma pasta.", pasta)
        resumo["erros"].append(f"Não é uma pasta: {pasta}")
        return resumo

    for item in sorted(caminho_pasta.iterdir()):
        if item.is_dir():
            continue  # não reprocessa subpastas já existentes

        try:
            extensao = obter_extensao(item.name)
            pasta_destino = caminho_pasta / extensao
            destino_final = destino_sem_conflito(pasta_destino, item.name)

            if dry_run:
                logger.info("[SIMULAÇÃO] %s -> %s", item.name, destino_final)
                resumo["movidos"] += 1
                continue

            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(item), str(destino_final))
            logger.info("Movido: %s -> %s", item.name, destino_final)
            resumo["movidos"] += 1

        except (OSError, shutil.Error) as erro:
            logger.error("Falha ao mover '%s': %s", item.name, erro)
            resumo["erros"].append(f"{item.name}: {erro}")
            resumo["ignorados"] += 1

    logger.info(
        "Concluído. Movidos: %d | Ignorados: %d | Erros: %d",
        resumo["movidos"], resumo["ignorados"], len(resumo["erros"]),
    )
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser(description="Organiza arquivos de uma pasta por extensão.")
    parser.add_argument("pasta", help="Caminho da pasta a organizar")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula, sem mover arquivos")
    args = parser.parse_args()

    organizar_arquivos(args.pasta, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
```

**Principais alterações e justificativa:**

- `Path.suffix` substitui `nome.split(".")[-1]`, retornando `""` quando não há extensão — isso elimina a colisão de nomes entre arquivo e pasta que causava o `NotADirectoryError`. Arquivos sem extensão vão para `SEM_EXTENSAO/`.
- `destino_sem_conflito` verifica se o destino já existe e, em caso positivo, gera `nome_1.ext`, `nome_2.ext` etc., em vez de sobrescrever.
- `try/except (OSError, shutil.Error)` garante que a pasta inexistente (ou uma falha pontual em um arquivo) gera uma mensagem de erro tratada, e o programa continua/encerra de forma controlada, sem traceback cru para o usuário.
- Parâmetro `pasta` deixou de ser fixo no código — agora vem por linha de comando (`argparse`), tornando o script reutilizável.
- `--dry-run` permite simular a operação e conferir o resultado antes de mover arquivos de verdade — atende à recomendação do material ("simular antes da alteração real").
- `logging` substitui `print`, dando um registro estruturado e mais fácil de redirecionar para um arquivo de log.
- `if __name__ == "__main__":` evita que o script execute automaticamente ao ser importado como módulo.
- A função retorna um `dict` de resumo, permitindo tanto uso via CLI quanto integração/teste programático.

## 12. Casos de Teste — Versão Refatorada

Reexecutei os mesmos três testes, mais um teste extra de colisão de nomes, contra a versão refatorada.

### Teste 1 — Caso normal (repetido)

```
$ python organiza_arquivos_v2.py t1
Movido: Relatorio João FINAL.pdf -> t1/PDF/Relatorio João FINAL.pdf
Movido: backup.zip -> t1/ZIP/backup.zip
Movido: foto_evento.jpg -> t1/JPG/foto_evento.jpg
Movido: notas.txt -> t1/TXT/notas.txt
Movido: planilha_vendas.xlsx -> t1/XLSX/planilha_vendas.xlsx
Movido: relatorio_maria.PDF -> t1/PDF/relatorio_maria.PDF
Movido: script.py -> t1/PY/script.py
Concluído. Movidos: 7 | Ignorados: 0 | Erros: 0
```
✅ Passou — mesmo comportamento da v1, sem regressão.

### Teste 2 — Caso limite (arquivo sem extensão)

```
$ python organiza_arquivos_v2.py t2
Movido: LICENSE -> t2/SEM_EXTENSAO/LICENSE
Movido: README -> t2/SEM_EXTENSAO/README
Concluído. Movidos: 2 | Ignorados: 0 | Erros: 0
```
✅ Passou — bug corrigido.

Testei também o subcaso de **pasta vazia**:
```
$ python organiza_arquivos_v2.py t2vazia
Concluído. Movidos: 0 | Ignorados: 0 | Erros: 0
```
✅ Passou, sem erro.

### Teste 3 — Caso de erro (pasta inexistente)

```
$ python organiza_arquivos_v2.py pasta_que_nao_existe
Erro: a pasta 'pasta_que_nao_existe' não existe.
```
✅ Passou — mensagem tratada, sem traceback.

### Teste extra — Colisão de nomes + `--dry-run`

Criei `t4/nota.txt` e já uma subpasta `t4/TXT/nota.txt` pré-existente, para forçar conflito:

```
$ python organiza_arquivos_v2.py t4 --dry-run
[SIMULAÇÃO] nota.txt -> t4/TXT/nota_1.txt

$ python organiza_arquivos_v2.py t4
Movido: nota.txt -> t4/TXT/nota_1.txt
Concluído. Movidos: 1 | Ignorados: 0 | Erros: 0
```
✅ Passou — nenhum arquivo sobrescrito; o script renomeou automaticamente para `nota_1.txt`, e o `--dry-run` previu corretamente o resultado antes da execução real.

## 13. Comparação entre Versões

| Critério | Versão inicial | Versão refatorada |
|---|:---:|:---:|
| Funcionamento correto | 2 | 5 |
| Clareza | 3 | 5 |
| Organização | 2 | 5 |
| Legibilidade | 3 | 4 |
| Tratamento de erros | 1 | 5 |
| Facilidade de manutenção | 2 | 5 |

A versão inicial funciona apenas no caminho feliz (arquivos com extensão, sem conflitos, pasta existente). A versão refatorada resolve os três problemas encontrados nos testes e agrega recursos que o enunciado original nem pedia explicitamente, mas que reduzem risco real de uso (dry-run, log, não sobrescrita).

## 14. Reflexão (Take Away)

**1. Em qual etapa a IA foi mais útil: geração, explicação, depuração, testes, refatoração ou documentação? Justifique.**
Na depuração e na refatoração. A geração inicial produziu algo plausível e até "funcional" à primeira vista, mas foi só ao testar contra casos-limite reais (arquivo sem extensão, pasta inexistente) que os defeitos apareceram. A IA foi mais valiosa quando usada para analisar *por que* cada erro acontecia e propor uma correção estruturada, e não apenas para gerar a primeira versão.

**2. Qual parte da solução exigiu mais raciocínio humano?**
Definir os casos de teste e interpretar os tracebacks. A IA sugere o código, mas decidir "o que pode dar errado nesta automação" (arquivo sem extensão colidindo com nome de pasta, risco de sobrescrita, pasta inexistente) exigiu pensar no problema de forma crítica, e não apenas aceitar a solução pronta.

**3. A primeira solução gerada funcionou? Se não, qual foi o problema?**
Funcionou apenas no caso normal (Teste 1). Falhou em dois dos três testes: quebrou com `NotADirectoryError` para arquivo sem extensão e com `FileNotFoundError` para pasta inexistente — ambos por ausência total de tratamento de erros e por uma lógica ingênua de extração de extensão (`split(".")[-1]`).

**4. O que mudou após a refatoração?**
A extração de extensão passou a usar `Path.suffix` (correta mesmo sem ponto no nome); qualquer erro de sistema de arquivos é capturado e reportado, sem travar o programa; conflitos de nome são resolvidos por renomeação automática em vez de sobrescrita silenciosa; e o script ganhou parametrização via linha de comando, modo de simulação (`--dry-run`) e log estruturado.

**5. Você conseguiria explicar o programa sem consultar a resposta da IA?**
Sim. A lógica central é simples: para cada arquivo, calcular a extensão, montar o caminho de destino, evitar conflito de nome e mover. As partes que exigiram mais atenção para eu realmente entender foram `Path.suffix` (comportamento com e sem ponto no nome) e o laço de `destino_sem_conflito`, que teria efeito colateral perigoso (loop infinito) se não houvesse garantia de que o contador sempre gera um nome novo — o que de fato acontece, pois `contador` cresce indefinidamente até achar um nome livre.

**6. Qual foi o principal risco identificado no uso da IA durante a atividade?**
Confiar cegamente na primeira versão só porque ela "parecia" correta e rodava sem erro em um teste manual rápido e não representativo. O risco real de automação de arquivos é destrutivo (mover/sobrescrever dados), então testar apenas o caminho feliz — como eu quase fiz — pode mascarar um bug que, em produção, apagaria ou perderia arquivos de um usuário real.

## 15. Desafio Final

"Programar com IA não significa deixar a IA programar por mim. Significa **usar a IA como um par de revisão acelerado — que gera hipóteses de solução rapidamente —, mantendo em mim, programador, a responsabilidade de definir o problema corretamente, testar contra casos reais e validar tecnicamente cada linha antes de considerar o código pronto para uso.**"

Cinco regras para um desenvolvedor utilizar IA de maneira responsável:

1. Nunca aceitar código gerado por IA sem antes entender o que cada trecho faz.
2. Sempre testar contra pelo menos um caso normal, um caso-limite e um caso de erro antes de considerar a solução pronta.
3. Nunca compartilhar credenciais, dados pessoais ou código proprietário em prompts.
4. Tratar a primeira versão gerada como rascunho, não como entrega — refatorar e revisar é parte do processo, não uma etapa opcional.
5. Assumir a responsabilidade técnica pelo código: se eu não consigo explicar ou defender uma linha, ela não deveria estar na minha entrega.

---

## Checklist de Entrega

- [x] Defini o problema.
- [x] Identifiquei entrada, processamento e saída.
- [x] Registrei o prompt utilizado.
- [x] Registrei a primeira versão do código.
- [x] Analisei criticamente a solução.
- [x] Executei pelo menos três testes.
- [x] Registrei os resultados.
- [x] Solicitei e analisei uma refatoração.
- [x] Comparei as versões.
- [x] Respondi à reflexão final.
- [ ] Organizei o arquivo no GitHub. *(pendente — depende do repositório do estudante)*
