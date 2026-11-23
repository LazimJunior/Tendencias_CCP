"""REG-01 a REG-13: regras de cada camada (percepção, decisão e execução)."""
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import apoio as a

_spec = importlib.util.spec_from_file_location("concurso", a.SCRIPT)
concurso = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(concurso)


class CamadaPerceptiva(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.work = a.preparar("numerado", self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_REG01_cabecalho_e_rodape_repetidos_sao_removidos(self):
        meta = a.ler(self.work, "meta.json")
        removidos = " ".join(meta["cabecalhos_rodapes_removidos"])
        self.assertIn("SEFIC/DF", removidos)
        self.assertIn("Pagina", removidos)
        self.assertNotIn("SEFIC/DF", (self.work / "programatico.txt").read_text(encoding="utf-8"))

    def test_REG02_armadilhas_de_numeracao_nao_quebram_topicos(self):
        d = a.disciplinas(a.ler(self.work, "verticalizado.json"))
        textos = {t["id_edital"]: t["texto"] for t in d["INFRAESTRUTURA"]["topicos"]}
        self.assertEqual(textos["1"], "Sistemas operacionais Windows 10 e 11 e Linux.")
        self.assertEqual(textos["3"], "ITIL V4: conceitos e práticas.")
        const = {t["id_edital"]: t["texto"] for t in d["NOÇÕES DE DIREITO CONSTITUCIONAL"]["topicos"]}
        self.assertIn("(art. 5 da Constituição Federal)", const["2"])
        self.assertIn("(arts. 37 a 41 da CF)", const["4"])
        leg = [t["texto"] for t in d["LEGISLAÇÃO"]["topicos"]]
        self.assertEqual(leg[0], "Lei nº 8.112/1990 e alterações.")
        self.assertNotIn("INFRAESTRUTURA", [k for k in d if k.startswith("ITIL")])

    def test_REG03_linha_quebrada_que_comeca_com_numero_nao_vira_item(self):
        linhas = [("1 DAS DISPOSIÇÕES", 1), ("1.1 O resultado será publicado no dia", 1),
                  ("12 DE OUTUBRO DE 2026, no Diário Oficial.", 1), ("1.2 Outro item.", 1)]
        itens = concurso.segment_body(linhas)
        self.assertEqual([i["id"] for i in itens], ["1", "1.1", "1.2"])
        self.assertIn("12 DE OUTUBRO DE 2026", itens[1]["texto"])
        tops, numerado = concurso.split_topicos("1 Alfa. 2 Beta, prazo de. 9 Dias úteis. 3 Gama.")
        self.assertTrue(numerado)
        self.assertEqual([t["id_edital"] for t in tops], ["1", "2", "3"])

    def test_REG04_assinatura_vira_observacao_final_sem_perda(self):
        v = a.ler(self.work, "verticalizado.json")
        self.assertNotIn("FULANO DE TAL", a.disciplinas(v))
        self.assertEqual(v["observacoes_finais"][0], "FULANO DE TAL")
        self.assertIn("legislação com entrada em vigor", v["observacoes"][0])

    def test_REG05_ligaduras_e_caracteres_invisiveis_normalizados(self):
        self.assertEqual(concurso.nfc("deﬁciência clas­siﬁcados​"), "deficiência classificados")
        itens = {i["id"]: i["texto"] for i in a.ler(self.work, "itens.json")}
        self.assertIn("deficiência", itens["2.1.3"])

    def test_REG06_hifenizacao_preserva_o_texto(self):
        self.assertEqual(concurso.join_lines(["pós-", "graduação em com-", "putação"]), "pós-graduação em com-putação")


class CamadaDecisoria(unittest.TestCase):
    def test_REG07_bloco_movido_sem_perda_e_aviso_e_nao_reprovacao(self):
        src = "A B C D. E F G H. I J K L."
        linhas, ok = concurso.diff_report("x", src, "I J K L. A B C D. E F G H.")
        self.assertTrue(ok)
        self.assertIn("Movido (sem perda): 1", linhas[2])

    def test_REG08_copia_em_outro_cargo_nao_mascara_omissao(self):
        bloco = "LÍNGUA PORTUGUESA 1 Interpretação de textos. 2 Ortografia oficial. 3 Crase. "
        src = bloco * 3
        out = bloco * 2 + bloco.replace("2 Ortografia oficial. ", "")
        _, ok = concurso.diff_report("x", src, out)
        self.assertFalse(ok)

    def test_REG09_citacao_aceita_data_por_extenso_e_rejeita_numero_inventado(self):
        with tempfile.TemporaryDirectory() as t:
            work = a.preparar("numerado", t)
            base = {"secao": "x", "item": "4.3", "trecho": "terão a data provável de 12 de outubro de 2026"}
            a.gravar(work, "ficha.json", {"campos": [dict(base, campo="ok", valor="12/10/2026")]})
            self.assertEqual(a.rodar("citacoes", "-w", work).returncode, 0)
            a.gravar(work, "ficha.json", {"campos": [dict(base, campo="errado", valor="19/10/2026")]})
            self.assertEqual(a.rodar("citacoes", "-w", work).returncode, 1)

    def test_REG10_comparar_lista_inclusoes_exclusoes_e_alteracoes(self):
        def v(topicos):
            return {"grupos": [{"grupo": ["G"], "disciplinas": [{"disciplina": "D", "topicos": topicos}]}]}
        antigo = v([{"id_edital": "1", "texto": "A."}, {"id_edital": "2", "texto": "B."}, {"id_edital": "3", "texto": "C."}])
        novo = v([{"id_edital": "1", "texto": "A."}, {"id_edital": "2", "texto": "B alterado."}, {"id_edital": "4", "texto": "D."}])
        with tempfile.TemporaryDirectory() as t:
            pa, pb = Path(t) / "a.json", Path(t) / "b.json"
            pa.write_text(json.dumps(antigo), encoding="utf-8")
            pb.write_text(json.dumps(novo), encoding="utf-8")
            out = a.rodar("comparar", pa, pb).stdout
        self.assertIn("antes: 2 B.", out)
        self.assertIn("depois: 2 B alterado.", out)
        self.assertIn("incluído: 4 D.", out)
        self.assertIn("removido: 3 C.", out)


class CamadaExecutiva(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name)
        cls.work = a.preparar("numerado", cls.tmp)
        a.gravar(cls.work, "ficha.json", a.ef.FICHA_NUMERADO)
        a.gravar(cls.work, "pesos.json", a.ef.PESOS_NUMERADO)
        cls.vault = cls.tmp / "vault"
        r = a.rodar("obsidian", "-w", cls.work, "--nome", "Teste 2026", "--saida", cls.vault, "--horas", "12")
        assert r.returncode == 0, r.stdout + r.stderr
        cls.pasta = cls.vault / "Teste 2026"

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_REG11_painel_dataview_tem_javascript_valido(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js não instalado")
        painel = (self.pasta / "00 Painel.md").read_text(encoding="utf-8")
        blocos = re.findall(r"```dataviewjs\n(.*?)```", painel, re.S)
        self.assertEqual(len(blocos), 5)
        for i, b in enumerate(blocos):
            js = self.tmp / f"b{i}.js"
            js.write_text("(async () => {\n" + b + "\n})();", encoding="utf-8")
            r = subprocess.run([node, "--check", str(js)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_REG12_notas_de_disciplina_tem_checklist_literal_e_pesos(self):
        nota = (self.pasta / "Disciplinas" / "Língua Portuguesa.md").read_text(encoding="utf-8")
        self.assertIn("questoes: 20", nota)
        self.assertIn("questoes_estimado: true", nota)
        self.assertIn("- [ ] **1** Compreensão e interpretação de textos de gêneros variados. ^t-1", nota)
        self.assertIn("\t- [ ] **4.1** Emprego de elementos de referenciação", nota)
        ficha = (self.pasta / "01 Ficha.md").read_text(encoding="utf-8")
        self.assertIn("[[03 Edital Integral#^i-5-4\\|item 5.4]]", ficha)

    def test_REG13_planilha_e_anki(self):
        from openpyxl import load_workbook
        xlsx = self.pasta / "v.xlsx"
        self.assertEqual(a.rodar("xlsx", "-w", self.work, "--saida", xlsx).returncode, 0)
        wb = load_workbook(xlsx)
        self.assertEqual(wb["Verticalizado"].max_row - 1, 29)
        self.assertEqual(wb["Prioridade"]["H4"].value, "=D4*G4*(1-F4/5)")
        anot = self.pasta / "Anotações" / "Teste.md"
        anot.write_text('---\ndisciplina: "Legislação"\n---\nprazo:: 30 dias\n## Flashcards\nQual a LGPD?::Lei 13.709/2018\n',
                        encoding="utf-8")
        saida = self.tmp / "anki.txt"
        r = a.rodar("anki", self.pasta, "--saida", saida)
        self.assertIn("1 cartões", r.stdout)
        linhas = saida.read_text(encoding="utf-8").splitlines()
        self.assertEqual(linhas[-1].split("\t")[:2], ["Qual a LGPD?", "Lei 13.709/2018"])

    def test_REG14_ficha_agrupa_secao_repetida_num_bloco_so(self):
        work = self.tmp / "work-secoes"
        shutil.copytree(self.work, work)
        a.gravar(work, "ficha.json", {"campos": [
            {"secao": "Identificação", "campo": "Banca", "valor": "IES", "item": "1.1"},
            {"secao": "Cronograma", "campo": "Provas", "valor": "12/10/2026", "item": "4.3"},
            {"secao": "Identificação", "campo": "Local", "valor": "Brasília/DF", "item": "1.3"},
        ]})
        r = a.rodar("obsidian", "-w", work, "--nome", "Secoes", "--saida", self.tmp / "vault-secoes")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ficha = (self.tmp / "vault-secoes" / "Secoes" / "01 Ficha.md").read_text(encoding="utf-8")
        self.assertEqual(ficha.count("## Identificação"), 1)
        self.assertLess(ficha.index("| Local |"), ficha.index("## Cronograma"))


if __name__ == "__main__":
    unittest.main()
