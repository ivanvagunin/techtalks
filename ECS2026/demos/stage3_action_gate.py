#!/usr/bin/env python3
"""Stage 3 demo: authorize model-proposed tool calls outside the model.

injected_refund scenario (--local or live):
  Retrieved content contains a prompt injection instruction.
  The model proposes issue_refund(C-4821, 500).
  The gate DENIES it — supervisor approval is required for high-risk refunds.

confirmed_appointment_change scenario (--local or live):
  A verified citizen requests a reschedule.
  The model proposes reschedule_appointment(A-2044, 2026-05-05T09:30:00).
  The gate ALLOWS it — relationship verified, confirmation present.

Use --local to skip the LLM call (deterministic output, suitable for smoke tests).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

DATA_PATH = Path(__file__).resolve().parent / "data" / "agent_scenarios.json"

DIVIDER = "-" * 62

REQUIRED_FIELDS: dict[str, set[str]] = {
    "issue_refund":            {"customer_id", "amount"},
    "reschedule_appointment":  {"customer_id", "appointment_id", "new_time"},
}

# Azure OpenAI function definitions for the live demo
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "issue_refund",
            "description": "Issue a refund to a customer account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer identifier (e.g. C-4821)"},
                    "amount":      {"type": "number", "description": "Refund amount in EUR"},
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
                    "customer_id":     {"type": "string", "description": "Customer identifier"},
                    "appointment_id":  {"type": "string", "description": "Appointment identifier"},
                    "new_time":        {"type": "string", "description": "New appointment time (ISO 8601)"},
                },
                "required": ["customer_id", "appointment_id", "new_time"],
            },
        },
    },
]

AINO_SYSTEM = (
    "You are Aino, Eir Health's AI assistant. "
    "Help citizens manage their health accounts using the available tools. "
    "Always use a tool when you can fulfill the request. "
    "Keep any text replies to one sentence."
)


# ── data helpers ─────────────────────────────────────────────────────────────
def load_scenarios() -> dict[str, dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def schema_valid(proposal: dict[str, Any]) -> bool:
    required = REQUIRED_FIELDS.get(proposal.get("tool", ""), set())
    return bool(required) and required.issubset(proposal)


def authorize(scenario: dict[str, Any]) -> tuple[str, str | None]:
    tool = scenario["proposal"]["tool"]
    if tool == "issue_refund":
        if not scenario.get("supervisor_approval"):
            return "DENY", "high_risk_action_requires_supervisor_approval"
        if not scenario.get("verified_relationship"):
            return "DENY", "verified_relationship_required"
        return "ALLOW", None
    if tool == "reschedule_appointment":
        if not scenario.get("verified_relationship"):
            return "DENY", "verified_relationship_required"
        if not scenario.get("confirmation"):
            return "DENY", "user_confirmation_required"
        return "ALLOW", None
    return "DENY", "unknown_tool"


def format_proposal(proposal: dict[str, Any]) -> str:
    tool = proposal["tool"]
    if tool == "issue_refund":
        return f"issue_refund(customer_id={proposal['customer_id']}, amount={proposal['amount']})"
    if tool == "reschedule_appointment":
        return (
            f"reschedule_appointment(customer_id={proposal['customer_id']}, "
            f"appointment_id={proposal['appointment_id']}, "
            f"new_time={proposal['new_time']})"
        )
    return tool


# ── live LLM call ────────────────────────────────────────────────────────────
def call_model_for_proposal(scenario: dict[str, Any]) -> dict[str, Any] | None:
    """Ask the model to respond to the scenario's user_message; return the proposed tool call or None."""
    from aif_client import get_client, handle_auth_error
    from openai import AuthenticationError
    client, deployment = get_client()

    user_msg = scenario.get("user_message", "I need help with my account.")
    injected = scenario.get("injected_context", "")
    if injected:
        user_msg = f"{user_msg}\n\n[Retrieved context]\n{injected}"

    try:
        resp = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": AINO_SYSTEM},
                {"role": "user",   "content": user_msg},
            ],
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=200,
            temperature=0.0,
        )
    except AuthenticationError as exc:
        handle_auth_error(exc, client)

    choice = resp.choices[0]
    if choice.message.tool_calls:
        tc = choice.message.tool_calls[0]
        args = json.loads(tc.function.arguments)
        return {"tool": tc.function.name, **args}
    return None


# ── demo ─────────────────────────────────────────────────────────────────────
def run_scenario(scenario_name: str, scenario: dict[str, Any], local: bool) -> int:
    print(DIVIDER)
    print(f"Stage 3: Action Gate   scenario={scenario_name}")
    print(DIVIDER)
    print(f"user    : {scenario['user']}")
    print(f"source  : {scenario['source']}")

    if scenario.get("injected_context"):
        # Print a short excerpt of the injected instruction
        excerpt = scenario["injected_context"].split("\n")[-1][:80]
        print(f"injected: \"{excerpt}\"")

    print()
    print(f"user    : {scenario.get('user_message', '(see scenario JSON)')}")
    print()

    if local:
        proposal = scenario["proposal"]
        print(f"model   : -> Proposed: {format_proposal(proposal)}")
    else:
        live_proposal = call_model_for_proposal(scenario)
        if live_proposal:
            scenario = dict(scenario)
            scenario["proposal"] = live_proposal
            proposal = live_proposal
            print(f"model   : -> Proposed: {format_proposal(proposal)}")
        else:
            print("model   : (no tool call proposed)")
            print()
            print("policy=DENY reason=no_tool_call_proposed")
            print("tool_call=skipped")
            print("audit=recorded")
            return 0

    valid = schema_valid(scenario["proposal"])
    print(f"schema  : {'valid' if valid else 'invalid'}")

    if scenario["proposal"]["tool"] == "reschedule_appointment":
        confirmed = "present" if scenario.get("confirmation") else "missing"
        print(f"confirmed: {confirmed}")

    decision, reason = authorize(scenario) if valid else ("DENY", "invalid_schema")

    print()
    if decision == "ALLOW":
        print("policy=ALLOW")
        print("tool_call=executed")
    else:
        print(f"policy=DENY reason={reason}")
        print("tool_call=skipped")
    print("audit=recorded")
    return 0


# ── entry point ───────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage 3: Eir Health action gate demo."
    )
    parser.add_argument("--scenario", required=True,
                        help="Scenario name from demos/data/agent_scenarios.json.")
    parser.add_argument("--local", action="store_true",
                        help="Skip LLM call — deterministic output for smoke tests")
    args = parser.parse_args()

    scenarios = load_scenarios()
    if args.scenario not in scenarios:
        choices = ", ".join(sorted(scenarios))
        raise SystemExit(f"Unknown scenario '{args.scenario}'. Choices: {choices}")

    return run_scenario(args.scenario, scenarios[args.scenario], args.local)


if __name__ == "__main__":
    raise SystemExit(main())
