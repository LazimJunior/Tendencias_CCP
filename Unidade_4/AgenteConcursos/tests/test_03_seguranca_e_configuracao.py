"""SEG-01 a SEG-06: configuração do agente, segredos e isolamento do worker."""
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import apoio as a

AGENTE = a.RAIZ / "agente"


class SegurancaEConfiguracao(unittest.TestCase):
    def test_SEG01_skill_respeita_o_formato_da_api(self):
        txt = (AGENTE / "skills" / "agente-concursos" / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", txt)
        self.assertIsNotNone(m)
        nome, desc = m.groups()
        self.assertRegex(nome, r"^[a-z0-9-]{1,64}$")
        self.assertNotRegex(nome, "anthropic|claude")
        self.assertLessEqual(len(desc), 1024)
        self.assertNotIn("<", desc)
        self.assertIn("scripts/concurso.py", txt)
        self.assertTrue((AGENTE / "skills" / "agente-concursos" / "scripts" / "concurso.py").is_file())

    def test_SEG02_system_prompt_tem_as_oito_partes(self):
        sp = (AGENTE / "system-prompt.md").read_text(encoding="utf-8")
        partes = ["PAPEL", "OBJETIVO", "CONTEXTO", "DADOS PERMITIDOS", "REGRAS DE DECISÃO",
                  "RESTRIÇÕES DE SEGURANÇA", "FORMATO DA RESPOSTA", "TRATAMENTO DE ERROS"]
        posicoes = [sp.find(f"# {p}\n") for p in partes]
        self.assertTrue(all(p >= 0 for p in posicoes), dict(zip(partes, posicoes)))
        self.assertEqual(posicoes, sorted(posicoes))
        self.assertIn("listas de candidatos", sp)
        self.assertIn("alertas_injecao", sp)

    def test_SEG03_agent_md_usa_o_mesmo_system_prompt(self):
        corpo = (AGENTE / "agent.md").read_text(encoding="utf-8").split("---\n", 2)[2].strip()
        self.assertEqual(corpo, (AGENTE / "system-prompt.md").read_text(encoding="utf-8").strip())

    def test_SEG04_repositorio_sem_credenciais(self):
        padroes = [r"sk-ant-(api|oat)\d{2}-[A-Za-z0-9_-]{20,}", r"ghp_[A-Za-z0-9]{30,}", r"AKIA[0-9A-Z]{16}"]
        for f in a.RAIZ.rglob("*"):
            if f.is_file() and ".git" not in f.parts and "saida" not in f.parts and f.suffix not in (".pdf", ".xlsx", ".pyc"):
                txt = f.read_text(encoding="utf-8", errors="ignore")
                for p in padroes:
                    self.assertIsNone(re.search(p, txt), f"possível credencial em {f.relative_to(a.RAIZ)}")
        gi = (a.RAIZ / ".gitignore").read_text(encoding="utf-8")
        for item in (".env", ".concurso-worker.env", "demo/saida/"):
            self.assertIn(item, gi)

    def test_SEG05_worker_isolado_no_wsl(self):
        sh = a.RAIZ / "worker" / "setup-wsl.sh"
        self.assertEqual(subprocess.run(["bash", "-n", str(sh)]).returncode, 0)
        txt = sh.read_text(encoding="utf-8")
        for trecho in ("[automount]\nenabled=false", "[interop]\nenabled=false", "appendWindowsPath=false",
                       "/workspace/vault drvfs", "chmod 600"):
            self.assertIn(trecho, txt)

    def test_SEG06_cliente_limita_gasto_e_exportacao_nao_sai_da_pasta(self):
        cli = (a.RAIZ / "cliente" / "sessao.py").read_text(encoding="utf-8")
        compile(cli, "sessao.py", "exec")
        self.assertIn('"max_list_cost"', cli)
        with tempfile.TemporaryDirectory() as t:
            work = a.preparar("numerado", t)
            saida = Path(t) / "vault"
            a.rodar("obsidian", "-w", work, "--nome", "../../fora", "--saida", saida)
            for f in Path(t).rglob("*.md"):
                if work in f.parents:
                    continue
                self.assertTrue(str(f.resolve()).startswith(str(saida.resolve())), f)


if __name__ == "__main__":
    unittest.main()
