#!/usr/bin/env python3
"""Stage 2 demo: permission-aware retrieval before prompt assembly.

Without policy (--policy off):
  All retrieved documents — including internal employee playbook and tenant-specific
  records — are injected into the model context. Aino leaks restricted content.

With policy (--policy on):
  The policy filter denies restricted documents before prompt assembly.
  Aino only sees public documents and gives an appropriate, limited response.

Use --local to skip the LLM call (deterministic output, suitable for smoke tests).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

DATA_PATH = Path(__file__).resolve().parent / "data" / "rag_documents.json"

USER_AUDIENCE: dict[str, set[str]] = {
    "public-user":    {"public"},
    "support-a":      {"public", "support"},
    "employee-a":     {"public", "support", "employee"},
    "tenant-b-support": {"public", "tenant-b-support"},
}

SYSTEM_PROMPT = """\
You are Aino, Eir Health's public-facing support chatbot.
Answer the user's question using ONLY the following retrieved documents.
Quote specific details from the documents in your response.
Keep your reply to 3-4 sentences.

Retrieved documents:
{documents}"""

DIVIDER = "-" * 62


# ── data helpers ─────────────────────────────────────────────────────────────
def load_documents() -> list[dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def allowed_for_user(document: dict[str, Any], user: str) -> bool:
    user_audience = USER_AUDIENCE.get(user, {"public"})
    return bool(user_audience & set(document["audience"]))


def ids(docs: list[dict[str, Any]]) -> str:
    return ", ".join(d["id"] for d in docs) if docs else "none"


def format_docs_for_prompt(docs: list[dict[str, Any]]) -> str:
    parts = []
    for d in docs:
        parts.append(f"[{d['title']}]\n{d['text']}")
    return "\n\n".join(parts)


# ── LLM call ─────────────────────────────────────────────────────────────────
def call_aino(docs: list[dict[str, Any]], query: str) -> str:
    from aif_client import get_client, handle_auth_error
    from openai import AuthenticationError
    client, deployment = get_client()
    try:
        resp = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(
                    documents=format_docs_for_prompt(docs))},
                {"role": "user", "content": query},
            ],
            max_tokens=220,
            temperature=0.3,
        )
    except AuthenticationError as exc:
        handle_auth_error(exc, client)
    return resp.choices[0].message.content.strip()


# ── demo modes ────────────────────────────────────────────────────────────────
def demo(user: str, query: str, policy: str, local: bool) -> int:
    documents = sorted(load_documents(), key=lambda d: d["score"], reverse=True)

    print(DIVIDER)
    label = "[policy=OFF]" if policy == "off" else "[policy=ON]"
    print(f"Stage 2: RAG Boundary   {label}")
    print(DIVIDER)
    print(f"user    : {user}")
    print(f"query   : \"{query}\"")
    print()

    if policy == "off":
        # Show all retrieved docs (unfiltered) — the vulnerability
        print("retrieved (unfiltered by vector similarity):")
        for d in documents:
            audience_str = ", ".join(d["audience"])
            print(f"  {d['id']:<40} score={d['score']}  [{audience_str}]")
        print()
        print(f"prompt_chunks={len(documents)}")
        print()
        if local:
            print(f"user    : {query}")
            print("aino    : [local mode — LLM call skipped]")
        else:
            print(f"user    : {query}")
            print()
            response = call_aino(documents, query)
            print(f"aino    : {response}")
        print()
        print("risk=restricted_content_entered_context")

    else:
        # Show all candidates, then apply policy filter
        retrieved = [d for d in documents if allowed_for_user(d, user)]
        denied    = [d for d in documents if not allowed_for_user(d, user)]

        print("candidates (by vector similarity):")
        for d in documents:
            allowed = allowed_for_user(d, user)
            verdict = "PASS" if allowed else "DENY"
            audience_str = ", ".join(d["audience"])
            print(f"  {verdict}  {d['id']:<40} score={d['score']}  [{audience_str}]")
        print()
        if denied:
            print("denied=" + ids(denied))
        print(f"prompt_chunks={len(retrieved)}")
        print()
        if local:
            print(f"user    : {query}")
            print("aino    : [local mode — LLM call skipped]")
        else:
            print(f"user    : {query}")
            print()
            response = call_aino(retrieved, query)
            print(f"aino    : {response}")
        print()
        print("risk=none")

    return 0


# ── entry point ───────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage 2: Eir Health RAG boundary demo."
    )
    parser.add_argument("--user",   required=True, help="User identity for retrieval policy.")
    parser.add_argument("--query",  required=True, help="Query text.")
    parser.add_argument("--policy", required=True, choices=("on", "off"),
                        help="off=no filter (shows vulnerability)  on=filter active (shows control)")
    parser.add_argument("--local",  action="store_true",
                        help="Skip LLM call — deterministic output for smoke tests")
    args = parser.parse_args()
    return demo(args.user, args.query, args.policy, args.local)


if __name__ == "__main__":
    raise SystemExit(main())

