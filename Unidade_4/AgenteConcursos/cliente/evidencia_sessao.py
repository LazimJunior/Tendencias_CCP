"""Gera os arquivos de evidência de uma sessão exportada pela API.

Uso: python3 evidencia_sessao.py <pasta_export> <prefixo> <saida_base> <titulo> [--completo]
  <pasta_export>/<prefixo>-detalhe.json e <prefixo>-eventos-N.json
  gera <saida_base>-resumo.json, -linha-do-tempo.md e -mensagens-do-agente.md
"""
import glob
import json
import re
import sys
from datetime import datetime, timedelta, timezone

BRT = timezone(timedelta(hours=-3))
MAX_LINHAS = 40
MAX_CHARS = 3000


def hora(ts):
    ts = re.sub(r"(\.\d{6})\d*", r"\1", ts.replace("Z", "+00:00"))
    return datetime.fromisoformat(ts).astimezone(BRT)


def texto(conteudo):
    partes = []
    for c in conteudo or []:
        if c.get("type") == "text":
            partes.append(c["text"])
        elif c.get("type") == "search_result":
            # Resultado de busca na web: so titulo e endereco. O texto e de terceiros e fica fora.
            partes.append(f"- {c.get('title', '?')} ({c.get('source', '?')})")
        else:
            partes.append(f"[{c.get('type', '?')}]")
    return "\n".join(partes)


def corta(t, completo):
    if completo:
        return t, False
    linhas = t.splitlines()
    cortado = False
    if len(linhas) > MAX_LINHAS:
        linhas = linhas[:MAX_LINHAS]
        cortado = True
    t2 = "\n".join(linhas)
    if len(t2) > MAX_CHARS:
        t2 = t2[:MAX_CHARS]
        cortado = True
    return t2, cortado


def cerca(t, lang="text"):
    n = 3
    while "`" * n in t:
        n += 1
    f = "`" * n
    return f"{f}{lang}\n{t}\n{f}"


def main():
    pasta, prefixo, base, titulo = sys.argv[1:5]
    completo = "--completo" in sys.argv
    det = json.load(open(f"{pasta}/{prefixo}-detalhe.json", encoding="utf-8"))
    arqs = sorted(glob.glob(f"{pasta}/{prefixo}-eventos-*.json"),
                  key=lambda x: int(re.search(r"-(\d+)\.json$", x).group(1)))
    ev = []
    for a in arqs:
        ev += json.load(open(a, encoding="utf-8"))["data"]

    resumo = dict(det)
    if "agent" in resumo and isinstance(resumo["agent"], dict) and "system" in resumo["agent"]:
        resumo["agent"] = dict(resumo["agent"])
        resumo["agent"]["system"] = "[omitido: idêntico a agente/system-prompt.md]"
    json.dump(resumo, open(f"{base}-resumo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    res = {e["tool_use_id"]: e for e in ev if e["type"] in ("user.tool_result", "agent.tool_result")}
    usos = [e for e in ev if e["type"] == "agent.tool_use"]
    modelo = [e for e in ev if e["type"] == "span.model_request_end"]
    criado = hora(det["created_at"])
    skill = ", ".join(s.get("version", "?") for s in det.get("agent", {}).get("skills", []))
    versao = det.get("agent", {}).get("version", "?")

    out = [f"# {titulo}: chamadas de ferramenta", ""]
    out.append(
        f"Sessão `{det['id']}`, criada em {criado:%d/%m/%Y} às {criado:%H:%M:%S} (horário de Brasília). "
        f"A API devolveu {len(ev)} eventos: {len(usos)} chamadas de ferramenta e {len(modelo)} chamadas ao modelo. "
        f"Agente na versão {versao}, skill na versão `{skill}`.")
    out.append("")
    if completo:
        out.append("Cada comando e cada saída aparecem completos.")
    else:
        out.append(
            f"Cada comando aparece inteiro. As saídas mostram até {MAX_LINHAS} linhas ou {MAX_CHARS} caracteres; "
            "quando há corte, ele vem marcado. O texto integral está nos JSON exportados.")
    out.append("")
    for i, e in enumerate(usos, 1):
        r = res.get(e["id"])
        erro = "sim" if r and r.get("is_error") else "não"
        out.append(f"## {i}. {hora(e['processed_at']):%H:%M:%S} · `{e['name']}` · erro: {erro}")
        out.append("")
        inp = e["input"]
        if e["name"] == "bash":
            out.append(cerca(inp.get("command", ""), "bash"))
        elif e["name"] == "write":
            c = inp.get("content", "")
            prev, cort = corta(c, completo)
            out.append(f"Arquivo: `{inp.get('file_path')}` ({len(c)} caracteres)")
            out.append("")
            out.append(cerca(prev + ("\n[… conteúdo cortado …]" if cort else "")))
        elif e["name"] == "edit":
            out.append(f"Arquivo: `{inp.get('file_path')}`")
            out.append("")
            out.append("Trecho antigo:")
            out.append("")
            out.append(cerca(inp.get("old_string", "")))
            out.append("")
            out.append("Trecho novo:")
            out.append("")
            out.append(cerca(inp.get("new_string", "")))
        elif "file_path" in inp:
            out.append(f"Arquivo: `{inp.get('file_path')}`")
        else:
            out.append(cerca(json.dumps(inp, ensure_ascii=False, indent=1), "json"))
        out.append("")
        if r:
            t, cort = corta(texto(r.get("content")), completo)
            out.append(cerca(t + ("\n[… saída cortada …]" if cort else "")))
            out.append("")
    open(f"{base}-linha-do-tempo.md", "w", encoding="utf-8").write("\n".join(out))

    msgs = [f"# {titulo}: mensagens", "", f"Sessão `{det['id']}`. Texto exato devolvido pela API, sem edição.", ""]
    for e in ev:
        if e["type"] == "user.message":
            msgs += ["## Pedido enviado", "", texto(e.get("content")), ""]
        elif e["type"] == "agent.message":
            msgs += [f"## Resposta ({hora(e['processed_at']):%H:%M:%S})", "", texto(e.get("content")), ""]
    open(f"{base}-mensagens-do-agente.md", "w", encoding="utf-8").write("\n".join(msgs))
    print(f"ok: {len(ev)} eventos, {len(usos)} ferramentas, {len(modelo)} chamadas ao modelo")


if __name__ == "__main__":
    main()
