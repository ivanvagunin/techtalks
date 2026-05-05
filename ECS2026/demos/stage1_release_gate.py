#!/usr/bin/env python3
"""Stage 1 demo: data release gate for support tickets used as chatbot context.

Without gate (--gate off):
  Raw ticket (with PII, staff notes, secret token) is used directly as model context.
  Aino reveals sensitive information to the citizen.

With gate (--gate on):
  Gate scans the raw ticket and BLOCKS it.
  The approved redacted version is used instead.
  Aino gives a safe, policy-compliant response.

Use --local to skip the LLM call (deterministic output, suitable for smoke tests).
Use --input <file> for the legacy single-file scan mode (backward-compatible).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Ensure this script's directory is on sys.path so aif_client can be imported
# when the script is run from the repo root (e.g. python demos/stage1_release_gate.py).
sys.path.insert(0, str(Path(__file__).parent))

# ── sensitive-data patterns ──────────────────────────────────────────────────
PATTERNS = [
    ("email_address",       re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("customer_identifier", re.compile(r"\bC-\d{4,}\b")),
    ("staff_only_note",     re.compile(r"\[STAFF ONLY\]", re.IGNORECASE)),
    ("secret_like_token",   re.compile(r"\beir_live_[A-Za-z0-9_]+\b")),
]

DATA_DIR = Path(__file__).resolve().parent / "data"

SYSTEM_PROMPT = """\
You are Aino, Eir Health's public-facing support chatbot.
Help citizens with clinic hours, appointments, portal access, and billing.
Use the support case context below. Reference specific details from it in your reply.
Keep your reply to 3-4 sentences.

Support case context:
---
{context}
---"""

USER_MSG = "Hi, I have a question about my recent billing issue. Can you help me?"

DIVIDER = "-" * 62


# ── gate logic ───────────────────────────────────────────────────────────────
def scan(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS if pattern.search(text)]


def extract_lineage(text: str) -> str:
    m = re.search(r"^Lineage:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    return m.group(1) if m else "demo-ticket-042"


# ── LLM call ─────────────────────────────────────────────────────────────────
def call_aino(context: str) -> str:
    from aif_client import get_client, handle_auth_error
    from openai import AuthenticationError
    client, deployment = get_client()
    try:
        resp = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
                {"role": "user",   "content": USER_MSG},
            ],
            max_tokens=200,
            temperature=0.3,
        )
    except AuthenticationError as exc:
        handle_auth_error(exc, client)
    return resp.choices[0].message.content.strip()


# ── demo modes ───────────────────────────────────────────────────────────────
def demo_gate_off(local: bool) -> int:
    """Show what happens when no release gate is in place (the vulnerability)."""
    raw = (DATA_DIR / "raw_support_ticket.txt").read_text(encoding="utf-8")

    print(DIVIDER)
    print("Stage 1: Release Gate   [gate=OFF]")
    print(DIVIDER)
    print(f"context : raw_support_ticket.txt  (unscanned)")
    print(f"user    : {USER_MSG}")
    print()

    if local:
        print("aino    : [local mode — LLM call skipped]")
        print()
        print("risk    : raw_data_used_as_context  (PII, staff notes, tokens exposed)")
    else:
        response = call_aino(raw)
        print(f"aino    : {response}")
        print()
        print("risk    : raw_data_leaked_via_context")
    return 0


def demo_gate_on(local: bool) -> int:
    """Show the release gate blocking the raw ticket and using the safe version (the control)."""
    raw = (DATA_DIR / "raw_support_ticket.txt").read_text(encoding="utf-8")
    findings = scan(raw)

    print(DIVIDER)
    print("Stage 1: Release Gate   [gate=ON]")
    print(DIVIDER)
    print(f"file    : raw_support_ticket.txt")
    decision = "BLOCK" if findings else "ALLOW"
    print(f"decision: {decision}")
    if findings:
        print("findings: " + ", ".join(findings))
        print("release_record=not_created")
        print()
        print("-> Gate blocked raw ticket. Falling back to approved redacted version.")
        print()

    redacted = (DATA_DIR / "redacted_support_ticket.txt").read_text(encoding="utf-8")
    lineage = extract_lineage(redacted)
    print(f"lineage : {lineage}")
    print(f"user    : {USER_MSG}")
    print()

    if local:
        print("aino    : [local mode — LLM call skipped]")
    else:
        response = call_aino(redacted)
        print(f"aino    : {response}")
    print()
    print("risk    : none  |  release_record=created")
    return 0


# ── legacy --input mode (smoke test backward-compat) ─────────────────────────
def legacy_input(path: Path) -> int:
    """Original single-file scan mode — produces deterministic output for smoke tests."""
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    text = path.read_text(encoding="utf-8")
    findings = scan(text)
    print(f"file={path.as_posix()}")
    if findings:
        print("decision=BLOCK")
        print("findings=" + ", ".join(findings))
        print("release_record=not_created")
    else:
        print("decision=ALLOW")
        print("findings=none")
        print(f"lineage={extract_lineage(text)}")
        print("release_record=created")
    return 0


# ── entry point ───────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage 1: Eir Health data release gate demo."
    )
    parser.add_argument(
        "--gate", choices=("off", "on"), default="on",
        help="off=no gate (shows vulnerability)  on=gate active (shows control)",
    )
    parser.add_argument(
        "--local", action="store_true",
        help="Skip LLM call — deterministic output for smoke tests",
    )
    # Legacy flag kept for backward compatibility with provision_demo_env.py smoke tests
    parser.add_argument("--input", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.input:
        return legacy_input(args.input)
    if args.gate == "off":
        return demo_gate_off(args.local)
    return demo_gate_on(args.local)


if __name__ == "__main__":
    raise SystemExit(main())

