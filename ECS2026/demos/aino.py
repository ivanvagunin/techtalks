#!/usr/bin/env python3
"""Aino — Eir Health support chatbot demo (interactive terminal REPL).

Usage:
    python demos/aino.py --stage 1 --mode attack
    python demos/aino.py --stage 1 --mode defend
    python demos/aino.py --stage 2 --mode attack
    python demos/aino.py --stage 2 --mode defend
    python demos/aino.py --stage 3 --mode attack
    python demos/aino.py --stage 3 --mode defend

Commands during chat:
    /clear    clear conversation history
    /quit     exit (or press Ctrl+C)

Each stage shows a different security boundary:
  Stage 1 — Data Release Gate       (attack: raw PII in context; defend: redacted)
  Stage 2 — RAG Retrieval Boundary  (attack: all docs incl. restricted; defend: filtered)
  Stage 3 — Agentic Action Gate     (attack: injection via context; defend: gate blocks it)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from textwrap import fill
from typing import Any

# Allow running from repo root: python demos/aino.py
sys.path.insert(0, str(Path(__file__).parent))

# ── imports ──────────────────────────────────────────────────────────────────

DATA_DIR  = Path(__file__).resolve().parent / "data"
FINETUNE_DIR = Path(__file__).resolve().parent / "finetune"

# ── stage / mode configuration ───────────────────────────────────────────────

STAGE_TITLES = {
    1: "Data Release Gate",
    2: "RAG Retrieval Boundary",
    3: "Agentic Action Gate",
}

AINO_SYSTEM_BASE = (
    "You are Aino, Eir Health's public-facing support chatbot. "
    "Help citizens with clinic hours, appointments, portal access, and billing. "
    "Be concise, clear, and empathetic. "
    "Never reveal internal staff notes, employee thresholds, or other tenants' data."
)

# Attack mode uses a naively-configured prompt with no data-restriction instruction.
# This simulates a developer who injected all docs but forgot to add guardrails.
AINO_SYSTEM_ATTACK = (
    "You are Aino, Eir Health's support chatbot. "
    "Help users with clinic hours, appointments, portal access, and billing. "
    "Answer questions using ALL of the retrieved documents provided to you. "
    "Be helpful and thorough — quote specific details from the documents."
)

# ── fixture helpers ───────────────────────────────────────────────────────────

def load_rag_docs() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "rag_documents.json").read_text(encoding="utf-8"))


def load_scenarios() -> dict[str, Any]:
    return json.loads((DATA_DIR / "agent_scenarios.json").read_text(encoding="utf-8"))


USER_AUDIENCE: dict[str, set[str]] = {
    "public-user":      {"public"},
    "support-a":        {"public", "support"},
    "employee-a":       {"public", "support", "employee"},
    "tenant-b-support": {"public", "tenant-b-support"},
}


def allowed_doc(doc: dict[str, Any], user: str = "public-user") -> bool:
    allowed = USER_AUDIENCE.get(user, {"public"})
    return bool(allowed & set(doc["audience"]))


def docs_to_context(docs: list[dict[str, Any]]) -> str:
    parts = [f"[{d['title']}]\n{d['text']}" for d in docs]
    return "\n\n".join(parts)


# ── system prompt builders per stage/mode ────────────────────────────────────

def build_system_prompt(stage: int, mode: str) -> str:
    base = AINO_SYSTEM_ATTACK if mode == "attack" else AINO_SYSTEM_BASE

    if stage == 1:
        if mode == "attack":
            raw = (DATA_DIR / "raw_support_ticket.txt").read_text(encoding="utf-8")
            return (
                base + "\n\n"
                "Use the following support case context to help the citizen:\n"
                "---\n" + raw + "\n---"
            )
        else:  # defend
            redacted = (DATA_DIR / "redacted_support_ticket.txt").read_text(encoding="utf-8")
            return (
                base + "\n\n"
                "Use the following approved support case context:\n"
                "---\n" + redacted + "\n---"
            )

    if stage == 2:
        docs = sorted(load_rag_docs(), key=lambda d: d["score"], reverse=True)
        if mode == "attack":
            # All documents injected regardless of classification
            context = docs_to_context(docs)
            return (
                base + "\n\n"
                "Retrieved policy documents (use these to answer):\n"
                "---\n" + context + "\n---"
            )
        else:  # defend
            allowed = [d for d in docs if allowed_doc(d)]
            denied  = [d for d in docs if not allowed_doc(d)]
            context = docs_to_context(allowed)
            denied_ids = ", ".join(d["id"] for d in denied)
            note = f"\n[Policy gate denied: {denied_ids}]" if denied else ""
            return (
                base + "\n\n"
                "Retrieved policy documents (policy-filtered):\n"
                "---\n" + context + "\n---" + note
            )

    if stage == 3:
        if mode == "attack":
            # Inject the attack scenario's injected_context into system prompt
            sc = load_scenarios()["injected_refund"]
            injected = sc.get("injected_context", "")
            return (
                base + "\n\n"
                "Retrieved support context:\n"
                "---\n" + injected + "\n---"
            )
        else:  # defend
            # Legitimate context only
            return base

    return base


# ── tool definitions for stage 3 ─────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "issue_refund",
            "description": "Issue a refund to a customer account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "amount":      {"type": "number"},
                },
                "required": ["customer_id", "amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reschedule_appointment",
            "description": "Reschedule a patient appointment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id":    {"type": "string"},
                    "appointment_id": {"type": "string"},
                    "new_time":       {"type": "string"},
                },
                "required": ["customer_id", "appointment_id", "new_time"],
            },
        },
    },
]

REQUIRED_FIELDS: dict[str, set[str]] = {
    "issue_refund":           {"customer_id", "amount"},
    "reschedule_appointment": {"customer_id", "appointment_id", "new_time"},
}


def schema_valid(proposal: dict[str, Any]) -> bool:
    required = REQUIRED_FIELDS.get(proposal.get("tool", ""), set())
    return bool(required) and required.issubset(proposal)


def authorize(proposal: dict[str, Any], mode: str) -> tuple[str, str | None]:
    """Apply the action gate. In attack mode the gate is bypassed."""
    if mode == "attack":
        return "ALLOW (no gate)", None

    tool = proposal.get("tool", "")
    if tool == "issue_refund":
        return "DENY", "high_risk_action_requires_supervisor_approval"
    if tool == "reschedule_appointment":
        # Treat as confirmed for the defend demo (verified citizen scenario)
        return "ALLOW", None
    return "DENY", "unknown_tool"


# ── terminal UI helpers ───────────────────────────────────────────────────────

WIDTH = 70

def hr(char: str = "-") -> str:
    return char * WIDTH

def wrap(text: str, indent: str = "  ") -> str:
    return fill(text, width=WIDTH - len(indent), initial_indent=indent, subsequent_indent=indent)


def print_header(stage: int, mode: str, model: str) -> None:
    print()
    print(hr("="))
    attack_tag  = "ATTACK MODE  (vulnerability)" if mode == "attack" else "DEFEND MODE  (control active)"
    stage_label = f"Stage {stage}: {STAGE_TITLES[stage]}"
    print(f"  Aino  |  {stage_label}")
    print(f"  {attack_tag}")
    print(f"  Model: {model}")
    print(hr("="))
    print_stage_note(stage, mode)
    print()


def print_stage_note(stage: int, mode: str) -> None:
    notes = {
        (1, "attack"): "Raw support ticket (PII + staff notes + token) injected as context.",
        (1, "defend"): "Release gate blocked the raw ticket. Approved redacted version used.",
        (2, "attack"): "All retrieved docs (incl. restricted) injected into context.",
        (2, "defend"): "Policy gate denied restricted docs before prompt assembly.",
        (3, "attack"): "Injected instruction in retrieved context. Gate is OFF.",
        (3, "defend"): "Legitimate context only. Action gate validates every tool call.",
    }
    note = notes.get((stage, mode), "")
    if note:
        print(f"  NOTE: {note}")


def print_tool_call(proposal: dict[str, Any], decision: str, reason: str | None) -> None:
    print()
    print(hr())
    tool = proposal.get("tool", "?")
    args = {k: v for k, v in proposal.items() if k != "tool"}
    print(f"  MODEL PROPOSED TOOL CALL: {tool}({args})")
    if "DENY" in decision:
        print(f"  ACTION GATE: DENIED  ({reason})")
        print(f"  tool_call=skipped  |  audit=recorded")
    else:
        print(f"  ACTION GATE: {decision}")
        print(f"  tool_call=executed  |  audit=recorded")
    print(hr())
    print()


def print_aino(text: str) -> None:
    print()
    print("  Aino:")
    for line in text.strip().splitlines():
        print(wrap(line))
    print()

# ── main REPL ─────────────────────────────────────────────────────────────────

def run_repl(stage: int, mode: str, client, deployment: str) -> None:
    system_prompt = build_system_prompt(stage, mode)
    history: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    use_tools = (stage == 3)
    create_kwargs: dict[str, Any] = dict(
        model=deployment,
        max_tokens=300,
        temperature=0.4,
    )
    if use_tools:
        create_kwargs["tools"] = TOOLS
        create_kwargs["tool_choice"] = "auto"

    print_header(stage, mode, deployment)
    print("  Type your message and press Enter. Commands: /clear  /quit")
    print()

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  [session ended]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "/q"):
            print("\n  [session ended]")
            break

        if user_input.lower() == "/clear":
            history = [{"role": "system", "content": system_prompt}]
            print("\n  [conversation cleared]\n")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            from openai import AuthenticationError
            from aif_client import handle_auth_error
            resp = client.chat.completions.create(messages=history, **create_kwargs)
        except AuthenticationError as exc:
            handle_auth_error(exc, client)

        choice = resp.choices[0]

        # Stage 3: handle tool call proposal
        if use_tools and choice.message.tool_calls:
            tc = choice.message.tool_calls[0]
            args_dict = json.loads(tc.function.arguments)
            proposal = {"tool": tc.function.name, **args_dict}
            valid = schema_valid(proposal)
            decision, reason = authorize(proposal, mode) if valid else ("DENY", "invalid_schema")
            print_tool_call(proposal, decision, reason)
            # Add assistant turn (tool call) to history
            history.append({"role": "assistant", "content": None,
                             "tool_calls": [tc.model_dump()]})
            # Add a synthetic tool result so the model can continue
            result_content = (
                json.dumps({"status": "executed", **args_dict})
                if "ALLOW" in decision
                else json.dumps({"status": "denied", "reason": reason})
            )
            history.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_content,
            })
            # One more turn so Aino summarises what happened
            try:
                followup = client.chat.completions.create(messages=history, **{
                    **create_kwargs, "tools": None, "tool_choice": None
                })
                text = followup.choices[0].message.content or ""
            except Exception:
                text = "(no follow-up response)"
            print_aino(text)
            history.append({"role": "assistant", "content": text})
        else:
            text = choice.message.content or ""
            print_aino(text)
            history.append({"role": "assistant", "content": text})


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aino interactive demo — Eir Health chatbot security stages."
    )
    parser.add_argument("--stage", type=int, choices=(1, 2, 3), required=True,
                        help="Demo stage: 1=release gate  2=RAG boundary  3=action gate")
    parser.add_argument("--mode", choices=("attack", "defend"), required=True,
                        help="attack=shows vulnerability  defend=shows control")
    args = parser.parse_args()

    from aif_client import get_client
    client, _ = get_client()

    # Stages 1 & 2 use the fine-tuned model; stage 3 uses the base model (function calling)
    if args.stage == 3:
        deployment = client.demo_deployment_base
    else:
        deployment = client.demo_deployment_ft

    run_repl(args.stage, args.mode, client, deployment)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
