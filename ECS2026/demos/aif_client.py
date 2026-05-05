#!/usr/bin/env python3
"""Azure AI Foundry / Azure OpenAI client helper for Eir Health demo scripts."""

from __future__ import annotations

import os
from pathlib import Path


def _load_env() -> None:
    """Load demos/.env — always overrides existing environment variables."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value  # always override — .env is authoritative


def get_client():
    """Return (AzureOpenAI client, deployment_name).

    Loads credentials from demos/.env (always takes priority over existing
    environment variables).  Raises SystemExit with a diagnostic if credentials
    are missing or authentication fails.
    """
    try:
        from openai import AzureOpenAI
    except ImportError:
        raise SystemExit(
            "\nopenai package not found.\n"
            "Activate the venv and install requirements:\n"
            "  .venv\\Scripts\\Activate.ps1\n"
            "  pip install -r demos/requirements.txt\n"
        )

    _load_env()

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/") + "/"
    key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deployment_base = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    deployment_ft   = os.environ.get("AZURE_OPENAI_DEPLOYMENT_FT", "").strip()
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    if not os.environ.get("AZURE_OPENAI_ENDPOINT") or not key:
        raise SystemExit(
            "\nMissing Azure credentials.\n"
            "Copy demos\\.env.example to demos\\.env and fill in:\n"
            "  AZURE_OPENAI_ENDPOINT=https://<project>.cognitiveservices.azure.com\n"
            "  AZURE_OPENAI_API_KEY=<key>\n"
            "  AZURE_OPENAI_DEPLOYMENT=<deployment-name>\n"
            "  AZURE_OPENAI_API_VERSION=2025-01-01-preview\n"
        )

    key_hint = key[:4] + "..." if len(key) > 4 else "(empty)"

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version=api_version,
    )
    client._demo_meta = {  # noqa: SLF001
        "endpoint": endpoint,
        "api_version": api_version,
        "deployment_base": deployment_base,
        "deployment_ft":   deployment_ft or deployment_base,
        "key_hint": key_hint,
        "env_file": str(Path(__file__).parent / ".env"),
    }
    # Expose both deployments so callers can choose
    client.demo_deployment_base = deployment_base
    client.demo_deployment_ft   = deployment_ft or deployment_base
    return client, deployment_base


def handle_auth_error(exc, client) -> None:
    """Print a diagnostic and exit cleanly on Azure 401 errors."""
    m = getattr(client, "_demo_meta", {})
    raise SystemExit(
        f"\nAzure auth error (401).\n"
        f"Credentials loaded from: {m.get('env_file', 'demos/.env')}\n"
        f"  endpoint   : {m.get('endpoint', '?')}\n"
        f"  api_version: {m.get('api_version', '?')}\n"
        f"  deployment : {m.get('deployment', '?')}\n"
        f"  key prefix : {m.get('key_hint', '?')}\n\n"
        f"Check these match your Azure AI Foundry project → Settings → API keys.\n"
    ) from exc

