"""Funções de apoio dos testes.

Os testes chamam o script pela linha de comando, como o agente faz no worker. A variável
CONCURSO_PY permite apontar para outra cópia do script (é o que o teste de mutação usa).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "demo"))
import editais_ficticios as ef  # noqa: E402

SCRIPT = Path(os.environ.get("CONCURSO_PY", RAIZ / "agente" / "skills" / "agente-concursos" / "scripts" / "concurso.py"))
_PDFS = Path(tempfile.mkdtemp(prefix="editais_"))


def pdf(nome):
    """PDF fictício (gerado uma vez por execução da suíte)."""
    alvo = _PDFS / f"{nome}.pdf"
    if not alvo.exists():
        ef.gerar(nome, alvo)
    return alvo


def rodar(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, encoding="utf-8")


def preparar(nome, base):
    """extrair + segmentar; devolve a pasta de trabalho."""
    work = Path(base) / "work"
    r = rodar("extrair", pdf(nome), "-w", work)
    assert r.returncode == 0, r.stdout + r.stderr
    r = rodar("segmentar", "-w", work)
    assert r.returncode == 0, r.stdout + r.stderr
    return work


def ler(work, nome):
    return json.loads((Path(work) / nome).read_text(encoding="utf-8"))


def gravar(work, nome, dados):
    (Path(work) / nome).write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


def disciplinas(v):
    return {d["disciplina"]: d for g in v["grupos"] for d in g["disciplinas"]}


def limpar():
    shutil.rmtree(_PDFS, ignore_errors=True)
