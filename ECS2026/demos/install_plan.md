# Demo Environment Installation Plan

## Goal

Provision the Eir Health chatbot demo environment for the three-stage talk. Each stage runs a **real Azure OpenAI chatbot** to demonstrate:

- Stage 1: how raw support data leaks PII through the model (and how a release gate stops it).
- Stage 2: how unrestricted RAG leaks internal documents into model context (and how policy filtering stops it).
- Stage 3: how prompt injection causes the model to propose an unauthorized tool call (and how the action gate stops it).

The demos use Azure AI Foundry as the LLM backend. All three stages require credentials. A `--local` flag is available for each stage to skip the LLM call (useful for smoke-testing without credentials).

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.11+ | `python --version` |
| pip | bundled with Python |
| Azure AI Foundry project | with an Azure OpenAI deployment (gpt-4o or gpt-4o-mini) |
| Azure OpenAI endpoint + API key | from Foundry project settings or Azure OpenAI resource |

## Step 1 — Install Python dependencies

From the `ECS` directory:

```powershell
pip install -r demos/requirements.txt
```

This installs the `openai` package (Azure OpenAI SDK).

## Step 2 — Configure Azure AI Foundry credentials

Copy the credential template and fill in your values:

```powershell
Copy-Item demos\.env.example demos\.env
notepad demos\.env
```

Set the following in `demos/.env`:

```
AZURE_OPENAI_ENDPOINT=https://<your-project-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Find these values in **Azure AI Foundry** → your project → **Settings** → **API keys**,
or in the **Azure OpenAI** resource → **Keys and Endpoint**.

> **Security**: `demos/.env` is gitignored. Never commit credentials.

## Step 3 — Provision and smoke-test the environment

Run from the `ECS` directory:

```powershell
.\demos\provision_demo_env.ps1
```

If PowerShell script execution is restricted, run the Python provisioner directly:

```powershell
python demos/provision_demo_env.py
```

The provisioner will:
- verify Python 3.11+
- create fixture data files (`demos/data/`, `demos/fallback/`)
- verify that all three stage scripts exist
- check that `openai` is installed and `demos/.env` is present
- run smoke tests for all six demo commands (in `--local` mode, no LLM required)
- print the live demo commands

To force-refresh fixture files:

```powershell
.\demos\provision_demo_env.ps1 -Force
```

## Step 4 — Verify live LLM connectivity

Run one stage with the real model to confirm credentials work:

```powershell
python demos/stage1_release_gate.py --gate on
```

You should see Aino respond with a short, safe answer based on the redacted ticket.

## Live Demo Commands

### Stage 1 — Data Release Gate

```powershell
# Show the attack: Aino leaks PII from the raw ticket
python demos/stage1_release_gate.py --gate off

# Show the control: gate blocks raw ticket, Aino uses safe redacted version
python demos/stage1_release_gate.py --gate on
```

### Stage 2 — RAG Retrieval Boundary

```powershell
# Show the attack: all 3 docs (incl. employee playbook) enter context
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy off

# Show the control: policy filter denies restricted docs before prompt assembly
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy on
```

### Stage 3 — Agentic Action Gate

```powershell
# Show the attack: injected instruction causes model to propose unauthorized refund
python demos/stage3_action_gate.py --scenario injected_refund

# Show the control: legitimate request approved after gate checks pass
python demos/stage3_action_gate.py --scenario confirmed_appointment_change
```

## Expected Timing

- Provisioning (smoke tests only): 5–15 seconds
- Provisioning (including `pip install`): 30–60 seconds
- Each live stage: 5–15 seconds per command (Azure OpenAI latency)
- Stage 1 demo pair: ~45 seconds
- Stage 2 demo pair: ~45 seconds
- Stage 3 demo pair: ~45 seconds
- Total demo time with narration: 5–6 minutes

## Troubleshooting

**`python` opens the Microsoft Store**  
Install Python 3.11+ and ensure the real interpreter is on `PATH`. The PowerShell provisioner tries these candidates in order:
1. `.venv\Scripts\python.exe`
2. `py -3`
3. `python`
4. `python3`

**`openai` package not found**  
Run: `pip install -r demos/requirements.txt`

**`Missing Azure credentials`**  
Verify `demos/.env` exists and has `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` set.

**Azure authentication errors (401/403)**  
Check that the API key matches the endpoint. In Azure AI Foundry, go to: project → Settings → API access.

**Model deployment not found (404)**  
Verify `AZURE_OPENAI_DEPLOYMENT` matches the deployment name in your Azure AI Foundry project.

**Terminal output wraps badly**  
Increase font size to 16pt+ before presenting. The scripts print compact lines designed for 100-character terminals.

**LLM fails during the talk**  
Switch to screenshots in `demos/fallback/`. Stage scripts also accept `--local` to run without LLM for a quick non-live fallback:

```powershell
python demos/stage1_release_gate.py --gate on --local
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy on --local
python demos/stage3_action_gate.py --scenario injected_refund --local
```
