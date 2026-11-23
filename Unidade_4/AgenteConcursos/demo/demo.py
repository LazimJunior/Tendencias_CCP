"""Demonstração ponta a ponta, sem IA e sem conta na Anthropic.

Executa o mesmo script que o agente usa no worker (agente/skills/.../concurso.py) sobre um
edital fictício e grava um vault de exemplo em demo/saida/vault. As etapas que, em produção,
o modelo faz (preencher ficha.json e pesos.json) usam aqui respostas prontas, iguais às que
o agente deveria produzir.

Uso: python demo/demo.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "demo"))
import editais_ficticios as ef  # noqa: E402

SCRIPT = RAIZ / "agente" / "skills" / "agente-concursos" / "scripts" / "concurso.py"
SAIDA = RAIZ / "demo" / "saida"
VAULT = SAIDA / "vault"
WORK = VAULT / ".concursos-work" / "sefic-df-2026"


def etapa(titulo, *args):
    def rel(x):
        s = str(x)
        return s.replace(str(RAIZ) + "/", "").replace(str(RAIZ) + "\\", "")
    print(f"\n$ concurso.py {' '.join(rel(a) for a in args)}")
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, encoding="utf-8")
    linhas = rel(r.stdout + r.stderr).strip().splitlines()
    for linha in linhas[:14]:
        print("  " + linha)
    if len(linhas) > 14:
        print(f"  ... ({len(linhas) - 14} linhas omitidas)")
    print(f"  -> {titulo}: {'OK' if r.returncode == 0 else 'FALHOU (codigo ' + str(r.returncode) + ')'}")
    return r.returncode


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.rmtree(SAIDA, ignore_errors=True)
    pdf = ef.gerar("numerado", VAULT / "_editais" / "edital-sefic-2026.pdf")
    print(f"Edital fictício gerado: {pdf.relative_to(RAIZ)}")
    codigos = [
        etapa("Camada 1 - extração", "extrair", pdf, "-w", WORK),
        etapa("Camada 1 - segmentação", "segmentar", "-w", WORK),
        etapa("Camada 3 - cobertura", "cobertura", "-w", WORK),
    ]
    (WORK / "ficha.json").write_text(json.dumps(ef.FICHA_NUMERADO, ensure_ascii=False, indent=1), encoding="utf-8")
    (WORK / "pesos.json").write_text(json.dumps(ef.PESOS_NUMERADO, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n[ficha.json e pesos.json gravados como o modelo faria na Camada 2]")
    codigos.append(etapa("Camada 3 - citações", "citacoes", "-w", WORK))
    codigos.append(etapa("Camada 4 - vault", "obsidian", "-w", WORK, "--nome", "SEFIC-DF 2026 - Analista TI",
                         "--banca", "IES", "--data-prova", "2026-10-12", "--horas", "12", "--saida", VAULT / "Concursos"))
    codigos.append(etapa("Camada 4 - planilha", "xlsx", "-w", WORK, "--saida",
                         VAULT / "Concursos" / "SEFIC-DF 2026 - Analista TI" / "Verticalizado.xlsx", "--horas", "12"))
    codigos.append(etapa("Camada 4 - auditoria de código no vault", "auditar", VAULT))
    print("\nArquivos gerados no vault de exemplo:")
    for f in sorted((VAULT / "Concursos").rglob("*")):
        if f.is_file():
            print("  " + str(f.relative_to(VAULT)))
    ok = all(c == 0 for c in codigos)
    print(f"\nRESULTADO: {'todas as etapas aprovadas' if ok else 'há etapas com falha'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
