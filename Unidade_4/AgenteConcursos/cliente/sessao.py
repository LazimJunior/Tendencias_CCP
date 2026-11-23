"""Cliente de terminal para o Agente de Concursos (Claude Managed Agents).

Roda no Windows (PowerShell), fora do WSL, para a API key nao ficar ao alcance do agente.

Uso:
  pip install anthropic
  $env:ANTHROPIC_API_KEY  = "sk-ant-..."
  $env:CONCURSO_AGENT_ID  = "agent_..."
  $env:CONCURSO_ENV_ID    = "env_..."
  python sessao.py                         # nova sessao (teto padrao: US$ 3)
  python sessao.py --orcamento 5           # teto da sessao em US$
  python sessao.py --sessao sesn_...       # continua uma sessao existente
"""
import argparse
import os
import sys

import anthropic


def turno(client, sid, texto):
    with client.beta.sessions.events.stream(sid) as stream:
        client.beta.sessions.events.send(
            sid, events=[{"type": "user.message", "content": [{"type": "text", "text": texto}]}]
        )
        for ev in stream:
            if ev.type == "agent.message":
                for bloco in ev.content:
                    if bloco.type == "text":
                        print(bloco.text, end="", flush=True)
            elif ev.type == "agent.tool_use":
                print(f"\n  [{ev.name}]", flush=True)
            elif ev.type == "session.error":
                erro = getattr(ev, "error", None)
                print(f"\n[erro da sessao: {getattr(erro, 'message', 'desconhecido')}]")
                return
            elif ev.type == "session.status_idle":
                motivo = getattr(getattr(ev, "stop_reason", None), "type", None)
                if motivo == "budget_reached":
                    print("\n[teto de gasto da sessao atingido: inicie outra sessao ou aumente --orcamento]")
                elif motivo == "requires_action":
                    print("\n[o agente pediu uma confirmacao: aprove pelo Console]")
                return


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Chat com o Agente de Concursos")
    ap.add_argument("--sessao", help="ID de uma sessao existente (sesn_...)")
    ap.add_argument("--orcamento", type=float, default=3.0, help="teto de gasto da sessao em US$")
    ap.add_argument("--titulo", default="Estudos para concurso")
    a = ap.parse_args()

    client = anthropic.Anthropic()
    if a.sessao:
        sid = a.sessao
    else:
        sessao = client.beta.sessions.create(
            agent=os.environ["CONCURSO_AGENT_ID"],
            environment_id=os.environ["CONCURSO_ENV_ID"],
            title=a.titulo,
            budget={"type": "limit", "max_list_cost": {"amount": str(round(a.orcamento * 100)), "currency": "USD"}},
        )
        sid = sessao.id

    print(f"Sessao: {sid}")
    print("Digite 'sair' para encerrar. Sem resposta? Confira se o worker esta rodando no Ubuntu.\n")
    while True:
        try:
            msg = input("voce> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not msg:
            continue
        if msg.lower() in ("sair", "exit", "quit"):
            break
        turno(client, sid, msg)
        print("\n")
    print(f"\nPara continuar depois: python sessao.py --sessao {sid}")


if __name__ == "__main__":
    main()
