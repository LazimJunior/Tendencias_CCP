#!/usr/bin/env bash
# Prepara o Ubuntu (WSL) como worker self-hosted do Agente de Concursos.
# Uso, dentro do Ubuntu:
#   bash setup-wsl.sh "C:/Users/SEU_USUARIO/Documents/Obsidian/Estudos"
# (caminho Windows do seu vault do Obsidian, com barras normais "/")
set -euo pipefail

VAULT_WIN="${1:?Informe o caminho Windows do vault. Ex.: C:/Users/Junior/Documents/Obsidian/Estudos}"
ANT_VERSION="2.12.1"
ME="$(id -un)"
UID_N="$(id -u)"
GID_N="$(id -g)"

echo "==> Pacotes do sistema"
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip tesseract-ocr tesseract-ocr-por curl file unzip ca-certificates

echo "==> Bibliotecas Python usadas pelo concurso.py"
pip install --break-system-packages --upgrade pymupdf pdfplumber openpyxl pytesseract

echo "==> ant CLI (worker do Managed Agents)"
curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_amd64.tar.gz" \
  | sudo tar -xz -C /usr/local/bin ant
ant --version

echo "==> /workspace e ponto de montagem do vault"
sudo mkdir -p /workspace/vault
sudo chown "$ME" /workspace
# Sem -R: numa reexecucao o vault ja esta montado (e .obsidian somente leitura), e o chown recursivo falharia.
mountpoint -q /workspace/vault || sudo chown "$ME" /workspace/vault

echo "==> Isolamento: o WSL deixa de enxergar o C: inteiro e de executar .exe do Windows"
sudo tee /etc/wsl.conf >/dev/null <<EOF
[boot]
systemd=true

[user]
default=${ME}

[automount]
enabled=false
mountFsTab=true

[interop]
enabled=false
appendWindowsPath=false
EOF

echo "==> Monta SOMENTE a pasta do vault em /workspace/vault"
VAULT_ESC="$(printf '%s' "$VAULT_WIN" | sed 's/ /\\040/g')"
sudo sed -i '\#[[:space:]]/workspace/vault[[:space:]]#d' /etc/fstab
echo "${VAULT_ESC} /workspace/vault drvfs defaults,uid=${UID_N},gid=${GID_N},metadata 0 0" | sudo tee -a /etc/fstab >/dev/null

echo "==> .obsidian somente leitura para o agente (plugins rodam no Windows, fora do isolamento)"
# O Obsidian no Windows continua gravando normalmente; a restricao vale so dentro do WSL.
# O agente nao tem a senha do sudo, entao nao consegue desfazer a montagem.
sudo sed -i '\#^/workspace/vault/.obsidian[[:space:]]#d' /etc/fstab
echo "/workspace/vault/.obsidian /workspace/vault/.obsidian none bind,ro 0 0" | sudo tee -a /etc/fstab >/dev/null

echo "==> Arquivo de credenciais do worker"
if [ ! -f "$HOME/.concurso-worker.env" ]; then
  cat > "$HOME/.concurso-worker.env" <<'EOF'
export ANTHROPIC_ENVIRONMENT_ID="env_COLE_AQUI"
export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-COLE_AQUI"
EOF
fi
chmod 600 "$HOME/.concurso-worker.env"

echo "==> Script para gravar a chave do ambiente (sem mostrar na tela e sem ir para o historico)"
cat > "$HOME/gravar-chave.sh" <<'EOF'
#!/usr/bin/env bash
# Uso: ~/gravar-chave.sh env_...   (depois cole SO a environment key quando ele pedir)
set -euo pipefail
ENV_ID="${1:?Informe o ID do ambiente (env_...)}"
case "$ENV_ID" in env_*) ;; *) echo "ERRO: o ID do ambiente comeca com env_"; exit 1;; esac
read -rsp "Cole so a environment key (clique direito) e tecle Enter: " K; echo
K="${K//$'\r'/}"
case "$K" in
  sk-ant-*) ;;
  *) echo "ERRO: isso nao e a chave (${#K} caracteres, comeca com '${K:0:6}'). Nada foi gravado."; exit 1;;
esac
umask 077
printf 'export ANTHROPIC_ENVIRONMENT_ID="%s"\nexport ANTHROPIC_ENVIRONMENT_KEY="%s"\n' "$ENV_ID" "$K" > "$HOME/.concurso-worker.env"
chmod 600 "$HOME/.concurso-worker.env"
echo "ok: ${K:0:12}... (${#K} caracteres) gravada em ~/.concurso-worker.env"
EOF
chmod +x "$HOME/gravar-chave.sh"

echo "==> Script para iniciar o worker"
cat > "$HOME/iniciar-worker.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
source "$HOME/.concurso-worker.env"
if ! mountpoint -q /workspace/vault; then
  echo "ERRO: vault nao montado em /workspace/vault. Rode 'wsl --shutdown' no PowerShell e abra o Ubuntu de novo."
  exit 1
fi
if [ -d /mnt/c/Windows ]; then
  echo "AVISO: o C: esta acessivel dentro do WSL (isolamento inativo)."
fi
if ! findmnt -no OPTIONS /workspace/vault/.obsidian 2>/dev/null | tr ',' '\n' | grep -qx ro; then
  echo "AVISO: /workspace/vault/.obsidian nao esta somente leitura. Abra o vault no Obsidian uma vez e rode 'wsl --shutdown'."
fi
sudo -k 2>/dev/null || true   # descarta a senha do sudo em cache: o agente herda este terminal
echo "Worker ativo. Deixe esta janela aberta enquanto usa o agente. Ctrl+C encerra."
exec ant beta:worker poll --workdir /workspace --max-idle 30m
EOF
chmod +x "$HOME/iniciar-worker.sh"

cat <<EOF

PRONTO. Proximos passos:
  1) Gere a key no Console (Ambientes > seu ambiente > Gerar chave de ambiente) e rode:
       ~/gravar-chave.sh env_SEU_AMBIENTE      -> cole SO a key quando ele pedir
  2) No PowerShell do Windows: wsl --shutdown   (aplica o isolamento e a montagem)
  3) Abra o Ubuntu de novo e confira:
       ls /workspace/vault     -> deve listar as notas do seu vault
       ls /mnt/c               -> deve vir vazio (C: nao montado)
  4) Inicie o worker: ~/iniciar-worker.sh
EOF
