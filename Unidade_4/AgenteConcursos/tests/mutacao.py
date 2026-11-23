"""Teste de mutação: os testes percebem quando uma proteção é desligada?

Para cada defeito, o script faz uma cópia do concurso.py com a proteção desligada, roda a
suíte inteira contra a cópia (variável CONCURSO_PY) e conta quantos testes falharam.
Um defeito que não derruba nenhum teste indica uma lacuna na suíte.

Uso: python tests/mutacao.py
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAL = RAIZ / "agente" / "skills" / "agente-concursos" / "scripts" / "concurso.py"

DEFEITOS = [
    ("Cobertura ignora texto faltando", "return linhas, (not falt and not extra)", "return linhas, (not extra)"),
    ("Detecção de prompt injection desligada", "injecao = detectar_injecao(paginas)", "injecao = []"),
    ("Proteção do progresso desligada", "and not a.forcar:", "and False:"),
    ("Citação não confere os números do valor", 'if not c.get("derivado"):', "if False:"),
    ("Numeração aceita qualquer número", "def plausible(prev, cand):\n", "def plausible(prev, cand):\n    return True\n"),
    ("Ligaduras do PDF não são normalizadas", ".translate(LIGADURAS)", ""),
    ("Auditoria aceita qualquer bloco de código", 'if m.group("corpo").strip() not in permitidos:', "if False:"),
]


def rodar_suite(script):
    env = dict(os.environ, CONCURSO_PY=str(script))
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(RAIZ / "tests")],
                       capture_output=True, text=True, env=env, encoding="utf-8")
    saida = r.stdout + r.stderr
    total = int(re.search(r"Ran (\d+) test", saida).group(1))
    falhas = sum(int(n) for n in re.findall(r"(?:failures|errors)=(\d+)", saida))
    return total, falhas


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = ORIGINAL.read_text(encoding="utf-8")
    total, falhas = rodar_suite(ORIGINAL)
    print(f"Script original: {total} testes, {falhas} falhas\n")
    print("| Defeito introduzido | Testes que falharam |")
    print("|---|---|")
    nao_detectados = 0
    with tempfile.TemporaryDirectory() as t:
        for nome, de, para in DEFEITOS:
            assert de in base, f"trecho não encontrado para: {nome}"
            copia = Path(t) / "concurso.py"
            copia.write_text(base.replace(de, para, 1), encoding="utf-8")
            _, f = rodar_suite(copia)
            nao_detectados += f == 0
            print(f"| {nome} | {f} |")
    print(f"\nDefeitos detectados: {len(DEFEITOS) - nao_detectados} de {len(DEFEITOS)}")
    sys.exit(1 if nao_detectados or falhas else 0)


if __name__ == "__main__":
    main()
