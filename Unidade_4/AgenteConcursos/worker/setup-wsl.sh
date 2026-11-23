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
sudo chown -R "$ME" /workspace

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

echo "==> Arquivo de credenciais do worker"
if [ ! -f "$HOME/.concurso-worker.env" ]; then
  cat > "$HOME/.concurso-worker.env" <<'EOF'
export ANTHROPIC_ENVIRONMENT_ID="env_COLE_AQUI"
export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-COLE_AQUI"
EOF
fi
chmod 600 "$HOME/.concurso-worker.env"

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
echo "Worker ativo. Deixe esta janela aberta enquanto usa o agente. Ctrl+C encerra."
exec ant beta:worker poll --workdir /workspace --max-idle 30m
EOF
chmod +x "$HOME/iniciar-worker.sh"

cat <<EOF

PRONTO. Proximos passos:
  1) Edite ~/.concurso-worker.env com o ID e a key do ambiente (Console > Environments).
  2) No PowerShell do Windows: wsl --shutdown   (aplica o isolamento e a montagem)
  3) Abra o Ubuntu de novo e confira:
       ls /workspace/vault     -> deve listar as notas do seu vault
       ls /mnt/c               -> deve dar erro (C: isolado)
  4) Inicie o worker: ~/iniciar-worker.sh
EOF
