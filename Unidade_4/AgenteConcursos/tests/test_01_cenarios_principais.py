"""CEN-01 a CEN-10: os dez cenários principais do agente."""
import copy
import filecmp
import tempfile
import unittest
from pathlib import Path

import apoio as a


class CenariosPrincipais(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_CEN01_edital_numerado_vira_verticalizado_integral(self):
        """CEN-01 - edital numerado: disciplinas, tópicos e subtópicos corretos, cobertura 100%."""
        work = a.preparar("numerado", self.tmp)
        d = a.disciplinas(a.ler(work, "verticalizado.json"))
        self.assertEqual(list(d), ["LÍNGUA PORTUGUESA", "NOÇÕES DE DIREITO CONSTITUCIONAL", "LEGISLAÇÃO",
                                   "INFRAESTRUTURA", "BANCO DE DADOS"])
        ids = [t["id_edital"] for t in d["LÍNGUA PORTUGUESA"]["topicos"]]
        self.assertEqual(ids, ["1", "2", "3", "4", "4.1", "4.2", "5", "5.1", "5.2", "6"])
        self.assertEqual(d["LÍNGUA PORTUGUESA"]["topicos"][4]["nivel"], 2)
        r = a.rodar("cobertura", "-w", work)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("COBERTURA 100%", r.stdout)

    def test_CEN02_edital_sem_numeracao_e_com_anexos(self):
        """CEN-02 - tópicos separados só por ponto final e anexos fora do programático: nada se perde."""
        work = a.preparar("sem_numeracao", self.tmp)
        d = a.disciplinas(a.ler(work, "verticalizado.json"))
        self.assertEqual(len(d["LÍNGUA PORTUGUESA"]["topicos"]), 9)
        self.assertEqual(len(d["TECNOLOGIA DA INFORMAÇÃO"]["topicos"]), 5)
        ids = [i["id"] for i in a.ler(work, "itens.json")]
        self.assertIn("ANEXO I", ids)
        self.assertIn("ANEXO III", ids)
        self.assertEqual(a.rodar("cobertura", "-w", work).returncode, 0)

    def test_CEN03_dados_incompletos_sem_conteudo_programatico(self):
        """CEN-03 - sem conteúdo programático: o script para com orientação e não gera saída."""
        work = self.tmp / "work"
        self.assertEqual(a.rodar("extrair", a.pdf("sem_programatico"), "-w", work).returncode, 0)
        r = a.rodar("segmentar", "-w", work)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--inicio-linha", r.stdout + r.stderr)
        self.assertFalse((work / "verticalizado.json").exists())

    def test_CEN04_omissao_de_topico_pela_ia_reprova(self):
        """CEN-04 - o modelo "esquece" um subtópico: a cobertura reprova e mostra o trecho perdido."""
        work = a.preparar("numerado", self.tmp)
        v = a.ler(work, "verticalizado.json")
        lp = a.disciplinas(v)["LÍNGUA PORTUGUESA"]
        lp["topicos"] = [t for t in lp["topicos"] if t["id_edital"] != "4.2"]
        a.gravar(work, "verticalizado.json", v)
        r = a.rodar("cobertura", "-w", work)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FALTANDO", r.stdout)
        self.assertIn("Emprego de tempos e modos verbais", r.stdout)

    def test_CEN05_invencao_resumo_e_duplicacao_reprovam(self):
        """CEN-05 - três formas de "deixar mais direto": inventar, resumir e duplicar. Todas reprovam."""
        work = a.preparar("numerado", self.tmp)
        original = a.ler(work, "verticalizado.json")

        def tentar(alterar):
            v = copy.deepcopy(original)
            alterar(a.disciplinas(v))
            a.gravar(work, "verticalizado.json", v)
            return a.rodar("cobertura", "-w", work)

        def inventar(d):
            d["INFRAESTRUTURA"]["topicos"][3]["texto"] = "Endereçamento IPv4, IPv6 e sub-redes (VLSM)."

        def resumir(d):
            d["BANCO DE DADOS"]["topicos"][-1]["texto"] = "Business intelligence e demais temas."

        def duplicar(d):
            d["LEGISLAÇÃO"]["topicos"].append(dict(d["LEGISLAÇÃO"]["topicos"][0]))

        for nome, f in (("inventar", inventar), ("resumir", resumir), ("duplicar", duplicar)):
            with self.subTest(nome):
                r = tentar(f)
                self.assertEqual(r.returncode, 1, r.stdout)
                self.assertIn("NÃO CONFERE", r.stdout)

    def test_CEN06_ficha_com_citacao_invalida_reprova(self):
        """CEN-06 - ficha: valor divergente, item inexistente e trecho parafraseado reprovam; "NÃO CONSTA" é aceito."""
        work = a.preparar("numerado", self.tmp)
        ficha = copy.deepcopy(a.ef.FICHA_NUMERADO)
        a.gravar(work, "ficha.json", ficha)
        r = a.rodar("citacoes", "-w", work)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("não consta", r.stdout)
        erradas = [
            {"secao": "x", "campo": "Taxa", "valor": "R$ 95,00", "item": "3.2", "trecho": "O valor da taxa de inscrição será de R$ 90,00"},
            {"secao": "x", "campo": "Duração", "valor": "4 horas", "item": "4.9", "trecho": "duração de 4 horas"},
            {"secao": "x", "campo": "Local", "valor": "Brasília", "item": "1.3", "trecho": "as provas acontecerão em Brasília"},
        ]
        for campo in erradas:
            with self.subTest(campo["campo"]):
                a.gravar(work, "ficha.json", {"campos": [campo]})
                self.assertEqual(a.rodar("citacoes", "-w", work).returncode, 1)

    def test_CEN07_retificacao_aplicada_com_log_e_idempotente(self):
        """CEN-07 - retificação: aplica onde-se-lê/leia-se e inclusão, recusa trecho inexistente e pode ser reexecutada."""
        work = a.preparar("numerado", self.tmp)
        ret = [
            {"retificacao": "Edital nº 2", "item": "3.2", "onde_se_le": "O valor da taxa de inscrição será de R$ 90,00.",
             "leia_se": "O valor da taxa de inscrição será de R$ 85,00."},
            {"retificacao": "Edital nº 2", "item": "BD", "apos_trecho": "3 Bancos de dados NoSQL.", "inserir": "3.1 MongoDB e Redis."},
        ]
        a.gravar(work, "ret.json", ret)
        for _ in range(2):
            r = a.rodar("retificar", work / "ret.json", "-w", work)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(a.rodar("segmentar", "-w", work).returncode, 0)
            texto = (work / "texto.txt").read_text(encoding="utf-8")
            self.assertEqual(texto.count("R$ 85,00"), 1)
            self.assertEqual(texto.count("MongoDB e Redis"), 1)
        ids = [t["id_edital"] for t in a.disciplinas(a.ler(work, "verticalizado.json"))["BANCO DE DADOS"]["topicos"]]
        self.assertIn("3.1", ids)
        a.gravar(work, "ret.json", ret + [{"retificacao": "x", "item": "9", "onde_se_le": "trecho que não existe", "leia_se": "y"}])
        r = a.rodar("retificar", work / "ret.json", "-w", work)
        self.assertEqual(r.returncode, 1)
        self.assertIn("encontrado 0x", r.stdout)

    def test_CEN08_manipulacao_das_instrucoes_no_pdf(self):
        """CEN-08 - prompt injection dentro do edital: é sinalizado, não some do texto e não altera nada."""
        work = self.tmp / "work"
        r = a.rodar("extrair", a.pdf("com_injecao"), "-w", work)
        self.assertEqual(r.returncode, 0)
        self.assertIn("ALERTA DE SEGURANCA", r.stdout)
        alertas = a.ler(work, "meta.json")["alertas_injecao"]
        tipos = {x["tipo"] for x in alertas}
        self.assertIn("ordem para ignorar instrucoes", tipos)
        self.assertIn("pedido de exfiltracao", tipos)
        self.assertTrue(all(x["pagina"] == 2 for x in alertas))
        self.assertEqual(a.rodar("segmentar", "-w", work).returncode, 0)
        itens = {i["id"]: i["texto"] for i in a.ler(work, "itens.json")}
        self.assertIn("ignore as instruções anteriores", itens["3.3"])
        self.assertEqual(a.rodar("cobertura", "-w", work).returncode, 0)
        limpo = self.tmp / "limpo"
        a.rodar("extrair", a.pdf("numerado"), "-w", limpo)
        self.assertEqual(a.ler(limpo, "meta.json")["alertas_injecao"], [])

    def test_CEN11_injecao_que_pede_codigo_no_obsidian(self):
        """CEN-11 - injeção sem palavras clássicas, pedindo dataviewjs e plugin: é sinalizada e o texto fica no edital."""
        work = self.tmp / "work-obs"
        r = a.rodar("extrair", a.pdf("injecao_obsidian"), "-w", work)
        self.assertEqual(r.returncode, 0)
        self.assertIn("ALERTA DE SEGURANCA", r.stdout)
        alertas = a.ler(work, "meta.json")["alertas_injecao"]
        self.assertEqual({x["tipo"] for x in alertas}, {"pedido de codigo executavel no Obsidian"})
        self.assertTrue(all(x["pagina"] == 2 for x in alertas))
        self.assertEqual(a.rodar("segmentar", "-w", work).returncode, 0)
        self.assertEqual(a.rodar("cobertura", "-w", work).returncode, 0)

    def test_CEN09_progresso_marcado_nunca_e_sobrescrito(self):
        """CEN-09 - reexportar o mesmo concurso preserva os [x] marcados e gera _atualizacao-<data>."""
        work = a.preparar("numerado", self.tmp)
        vault = self.tmp / "vault"
        self.assertEqual(a.rodar("obsidian", "-w", work, "--nome", "Teste 2026", "--saida", vault).returncode, 0)
        nota = vault / "Teste 2026" / "Disciplinas" / "Legislação.md"
        marcado = nota.read_text(encoding="utf-8").replace("- [ ] **1**", "- [x] **1**", 1)
        nota.write_text(marcado, encoding="utf-8")
        r = a.rodar("obsidian", "-w", work, "--nome", "Teste 2026", "--saida", vault)
        self.assertEqual(r.returncode, 0)
        self.assertIn("NADA foi sobrescrito", r.stdout)
        self.assertEqual(nota.read_text(encoding="utf-8"), marcado)
        self.assertTrue(any(p.name.startswith("_atualizacao-") for p in (vault / "Teste 2026").iterdir()))

    def test_CEN10_mesma_entrada_mesma_saida(self):
        """CEN-10 - consistência: o mesmo edital, processado duas vezes, gera arquivos idênticos."""
        saidas = []
        for i in range(2):
            base = self.tmp / f"exec{i}"
            work = a.preparar("numerado", base)
            a.rodar("obsidian", "-w", work, "--nome", "Teste 2026", "--saida", base / "vault")
            saidas.append(base)
        for rel in ("work/itens.json", "work/verticalizado.json", "work/programatico.txt"):
            self.assertTrue(filecmp.cmp(saidas[0] / rel, saidas[1] / rel, shallow=False), rel)
        cmp = filecmp.dircmp(saidas[0] / "vault", saidas[1] / "vault")
        pendentes = [cmp]
        while pendentes:
            c = pendentes.pop()
            self.assertFalse(c.diff_files or c.left_only or c.right_only, (c.left, c.diff_files))
            pendentes.extend(c.subdirs.values())


if __name__ == "__main__":
    unittest.main()
