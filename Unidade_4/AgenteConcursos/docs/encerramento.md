# Encerramento depois da apresentação

Roteiro para desligar com segurança tudo o que a validação em campo criou. Faça **depois** da apresentação: sem as chaves, o agente para de funcionar.

## Ordem recomendada

| # | O quê | Onde | Por quê |
|---|---|---|---|
| 1 | Revogar a chave de API usada na validação | Console › Settings › API Keys › chave › Delete | A chave ficou gravada no Windows e passou por canais fora do Console durante a validação. Revogar é o único jeito de garantir que ela não sirva mais |
| 2 | Revogar a chave do ambiente | Console › Agentes › Ambientes › `notebook-wsl` › Chaves de ambiente › revogar | Quem tiver essa chave consegue receber o trabalho das próximas sessões deste ambiente (risco R1) |
| 3 | Apagar as sessões de teste | Console › Agentes › Sessões › abrir cada uma › Ações | As transcrições ficam guardadas até serem apagadas, com trechos do vault e dos editais |
| 4 | Arquivar o agente e o ambiente, se não for mais usar | Console › Agentes / Ambientes | Evita sessões criadas por engano |
| 5 | Apagar as variáveis do Windows | PowerShell, comandos abaixo | A chave revogada não serve mais, mas não precisa continuar no registro |
| 6 | Apagar a chave do ambiente do Ubuntu | Ubuntu, comando abaixo | Mesmo motivo |
| 7 | Conferir o saldo | Console › Billing | Registrar o custo total no relatório |

Sessões criadas na validação: `sesn_01NjucVhopBAyHbvnmw1FWfK` (edital fictício), `sesn_01MEx4sUmmjg62LGurvTe9uL` (ataque controlado) e as três dos editais reais e do OCR, listadas em [validacao-em-campo.md](validacao-em-campo.md).

## Comandos

**PowerShell** (passo 5):
```powershell
foreach ($v in "ANTHROPIC_API_KEY", "CONCURSO_AGENT_ID", "CONCURSO_ENV_ID") { [Environment]::SetEnvironmentVariable($v, $null, "User") }
$h = (Get-PSReadLineOption).HistorySavePath
(Get-Content $h) | Where-Object { $_ -notmatch 'sk-ant-' } | Set-Content $h
```

**Ubuntu** (passo 6):
```bash
shred -u ~/.concurso-worker.env 2>/dev/null || rm -f ~/.concurso-worker.env
```

## Opcional

| O quê | Comando | Atenção |
|---|---|---|
| Tirar do vault as pastas de trabalho dos testes | apagar `Obsidian Vault\.concursos-work\teste-injecao` e `teste-ocr` | Não afeta as pastas dos concursos |
| Remover o Ubuntu do WSL | `wsl --unregister Ubuntu` no PowerShell | **Apaga tudo** que está dentro do Ubuntu, sem volta. O vault fica intacto, porque mora no Windows |
| Voltar o Dataview ao padrão | Obsidian › Configurações › Dataview | Deixe *Enable JavaScript Queries* desligado, mesmo sem o agente |
