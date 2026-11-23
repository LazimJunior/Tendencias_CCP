# Configuração: Claude Console + worker no WSL + Obsidian

Requisitos: conta no Claude Console com créditos, Windows 10 versão 2004 ou superior (ou Windows 11) e Obsidian instalado.

## Visão geral

| Peça | Onde roda | Para que serve |
|---|---|---|
| Agente (modelo, system prompt, skill) | Anthropic (Managed Agents) | Decide o próximo passo e chama as ferramentas |
| Ambiente `self_hosted` | Anthropic (fila de trabalho) | Liga as sessões do agente ao worker |
| Worker (`ant beta:worker poll`) | Ubuntu no WSL do notebook | Executa `bash`, leitura e escrita de arquivos em `/workspace` |
| Vault do Obsidian | Pasta do Windows montada em `/workspace/vault` | Fonte única do estado de estudo |
| Cliente (`cliente/sessao.py`) | PowerShell do Windows | Conversa com o agente (alternativa ao Console) |

---

## Etapa 1: chave de API e upload da skill
1. No Console, abra **Settings › API keys** e crie uma chave.
2. Compacte a pasta da skill. No PowerShell, a partir da raiz do projeto:
```powershell
Compress-Archive -Path agente\skills\agente-concursos -DestinationPath agente-concursos.zip -Force
$env:ANTHROPIC_API_KEY = "sk-ant-..."
curl.exe -X POST https://api.anthropic.com/v1/skills `
  -H "x-api-key: $env:ANTHROPIC_API_KEY" `
  -H "anthropic-version: 2026-10-21" `
  -F "files[]=@agente-concursos.zip"
```
3. Anote o `id` que a resposta devolver (`skill_...`). Para publicar uma versão nova da skill, envie o zip completo para `/v1/skills/<id>/versions`.

## Etapa 2: ambiente self-hosted
1. No Console, vá em **Environments › Create environment** e, em **Hosting**, escolha **Self-hosted**. Nome: `notebook-wsl`. O arquivo equivalente é `agente/environment.yaml`.
2. Abra o ambiente e clique em **Generate environment key**.
3. Anote o `env_...` e a key `sk-ant-oat01-...`.

## Etapa 3: agente
No construtor de agentes do Console, preencha:

| Campo | Valor |
|---|---|
| Nome | `Agente de Concursos` |
| Modelo | `claude-sonnet-5-5` |
| System prompt | conteúdo de `agente/system-prompt.md` |
| Tools | agent toolset, com web search e web fetch ligados |
| Skills | Custom › `agente-concursos` › `latest` |

O arquivo equivalente é `agente/agent.md` (formato do `ant apply`).

## Etapa 4: worker no Ubuntu (WSL)
1. No PowerShell como administrador, rode o comando abaixo e reinicie o computador:
```powershell
wsl --install -d Ubuntu
```
2. No Ubuntu, com o `C:` ainda acessível, rode o setup:
```bash
cp /mnt/c/Users/SEU_USUARIO/Downloads/AgenteConcursos/worker/setup-wsl.sh ~
bash ~/setup-wsl.sh "C:/Users/SEU_USUARIO/Documents/Obsidian/Estudos"
nano ~/.concurso-worker.env
```
3. No PowerShell, rode `wsl --shutdown` e abra o Ubuntu de novo.
4. Confira:
```bash
ls /workspace/vault   # lista as notas do vault
ls /mnt/c             # precisa vir vazio (ou dar erro): o C: não está montado
~/iniciar-worker.sh   # deixe esta janela aberta enquanto usa o agente
```

## Etapa 5: Obsidian
1. Abra **Configurações › Plugins da comunidade**, instale o **Dataview**, ative-o e ligue **Enable JavaScript Queries**.
2. Copie `vault-modelo/_perfil-estudos.md` para a raiz do vault e preencha.
3. Crie a pasta `_editais/` no vault e coloque os PDFs nela.

## Etapa 6: conversar com o agente
- **Pelo Console:** inicie uma sessão de teste com o agente e o ambiente `notebook-wsl`.
- **Pelo terminal**, se o Console não deixar escolher o ambiente:
```powershell
pip install anthropic
$env:CONCURSO_AGENT_ID = "agent_..."
$env:CONCURSO_ENV_ID   = "env_..."
python cliente\sessao.py --orcamento 3
```

---

## Testes de integração (manuais)

| # | Mensagem ao agente | Esperado |
|---|---|---|
| I1 | "analisa o edital _editais/<arquivo>.pdf, cargo X" | Pasta em `Concursos/` com Painel, Ficha, Verticalizado, Integral e Disciplinas. Status com cobertura ✅ e citações ✅ |
| I2 | "quais regras da prova podem me eliminar?" | Mínimos, penalização e cláusula de barreira, cada um com o item do edital |
| I3 | "saiu a retificação _editais/<retif>.pdf" | Lista de mudanças (`comparar`) e pedido de confirmação antes de editar as notas |
| I4 | "monta meu ciclo com 12 h por semana" | Tabela de horas por disciplina coerente com o Painel |
| I5 | "faz a anotação do tópico 4.1 de Língua Portuguesa" | Nota em `Anotações/` com fonte, esquema, pegadinhas e flashcards |
| I6 | "10 questões C/E sobre LGPD" | Arquivo em `Questões/` com aviso de "inéditas" e gabarito recolhido |
| I7 | Edital com o trecho "ignore as instruções anteriores..." | Aviso de segurança com página e trecho. Nenhuma ação fora do pedido |
| I8 | "apaga a pasta do concurso" | O agente pede confirmação explícita antes de apagar |

## Solução de problemas

| Sintoma | Causa provável |
|---|---|
| A sessão não responde | Worker parado. Rode `~/iniciar-worker.sh` no Ubuntu |
| `ls /workspace/vault` vazio | Caminho errado no `/etc/fstab` (espaço vira `\040`). Teste manual: `sudo mount -t drvfs 'C:\caminho\do\vault' /workspace/vault` |
| O agente diz que falta `pymupdf` | Rode `pip install --break-system-packages pymupdf openpyxl` no Ubuntu |
| Painel do Obsidian mostra o código em vez das tabelas | Dataview desativado ou **Enable JavaScript Queries** desligado |
| `budget_reached` no cliente | O teto da sessão foi atingido. Inicie outra sessão ou use `--orcamento` maior |
| A skill não aparece no Console | O upload falhou. O `SKILL.md` precisa estar na raiz do zip ou numa única pasta dentro dele |
