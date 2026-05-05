# Eir Health Demo Environment

Three interactive chatbot demos for the talk **"Securing Conversational AI Architectures"**.

`aino.py` is the main demo app — a terminal REPL where you type prompts live.
Each stage runs in **attack mode** (shows the vulnerability) then **defend mode** (shows the control).
The chatbot uses a fine-tuned Azure AI Foundry model for stages 1–2 and the base model for stage 3.

---

## Prerequisites

| Requirement | Check | Notes |
|---|---|---|
| Python 3.11+ | `python --version` | Must be ≥ 3.11 |
| `openai` package | `pip show openai` | Install via step 2 below |
| Azure AI Foundry project | Azure portal | Needs Azure OpenAI deployments |
| Base model deployment | e.g. `gpt-4o` | Used for stage 3 (function calling) |
| Fine-tuned deployment | e.g. `gpt-4o-mini-aino-ft` | Used for stages 1 & 2 (see fine-tuning below) |

---

## Setup (run once)

### 1 — Activate the virtual environment and install dependencies

```powershell
cd C:\...\presentations\ECS
.\.venv\Scripts\Activate.ps1
pip install -r demos/requirements.txt
```

### 2 — Configure credentials

```powershell
Copy-Item demos\.env.example demos\.env
notepad demos\.env
```

Fill in:
```
AZURE_OPENAI_ENDPOINT=https://<your-project>.cognitiveservices.azure.com
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=gpt-4o          # base model (stage 3)
AZURE_OPENAI_DEPLOYMENT_FT=             # fine-tuned model (stages 1+2, see below)
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### 3 — Fine-tune Aino (takes 30–60 min, do this before the talk)

```powershell
python demos/finetune/run_finetune.py
```

This uploads training data and creates a fine-tuning job on Azure AI Foundry.
When it completes, deploy the model in the Foundry UI and set `AZURE_OPENAI_DEPLOYMENT_FT` in `.env`.

See `demos/finetune/FINETUNE.md` for step-by-step instructions.

### 4 — Provision and smoke-test

```powershell
.\demos\provision_demo_env.ps1
```

---

## Running the demo

All commands from the **`ECS` directory** with the venv active.

---

### Stage 1 — Data Release Gate

**Story**: The support team wants to reuse historical tickets as chatbot context.
The raw ticket contains citizen PII, staff-only notes, and a secret-like token.

**Attack** (raw ticket injected, no gate):
```powershell
python demos/aino.py --stage 1 --mode attack
```
Try asking: *"Hi, I have a question about my recent billing issue. Can you help me?"*
Aino will reference Maria's name, the `SPRING-WALKIN` campaign code, and staff details.

**Defend** (gate blocked raw ticket, approved version used):
```powershell
python demos/aino.py --stage 1 --mode defend
```
Same prompt. Aino gives a safe, policy-compliant answer with no PII or internal details.

---

### Stage 2 — RAG Retrieval Boundary

**Story**: Eir Health adds RAG. Three docs are retrieved — a public policy, an employee-only
playbook, and a confidential tenant record. All are semantically relevant.

**Attack** (all docs injected, no policy filter):
```powershell
python demos/aino.py --stage 2 --mode attack
```
Try asking: *"What are the refund exception thresholds?"*
Aino quotes internal employee thresholds and campaign codes to a public user.

**Defend** (policy filter denies restricted docs):
```powershell
python demos/aino.py --stage 2 --mode defend
```
Same prompt. Aino only knows the public policy and gives an appropriately limited answer.

---

### Stage 3 — Agentic Action Gate

**Story**: Aino gets tools — it can reschedule appointments and issue refunds.
A prompt injection attack embeds an instruction in retrieved context to force an unauthorized refund.

**Attack** (injection via context, no gate):
```powershell
python demos/aino.py --stage 3 --mode attack
```
Try asking: *"I need help with my account."*
The model proposes `issue_refund(customer_id=C-4821, amount=500)` based on the injected instruction.
With no gate, the tool call executes.

**Defend** (gate validates every tool call):
```powershell
python demos/aino.py --stage 3 --mode defend
```
Try asking: *"Please reschedule my appointment A-2044 to May 5th at 9:30 AM. I confirm this change."*
The gate allows the legitimate reschedule. Then show what happens with the refund injection — denied.

---

## Chat commands

| Command | Effect |
|---|---|
| `/clear` | Clear conversation history (keep same stage/mode) |
| `/quit` | Exit the chat |
| `Ctrl+C` | Exit the chat |

---

## Fallback

If Azure connectivity fails during the talk, use the individual stage scripts with `--local`:

```powershell
python demos/stage1_release_gate.py --gate on --local
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy on --local
python demos/stage3_action_gate.py --scenario injected_refund --local
```

Screenshots and recordings can be stored in `demos/fallback/`.

---

## Files in this folder

| File / Folder | Purpose |
|---|---|
| `aino.py` | **Main demo app** — interactive REPL, all stages |
| `.env.example` | Credential template — copy to `.env` |
| `requirements.txt` | Python dependencies (`openai`) |
| `aif_client.py` | Azure OpenAI client helper (shared) |
| `finetune/` | Training data + fine-tuning script |
| `finetune/training_data.jsonl` | 40 Eir Health support Q&A training examples |
| `finetune/validation_data.jsonl` | 10 validation examples |
| `finetune/run_finetune.py` | Script to upload data and start the fine-tuning job |
| `finetune/FINETUNE.md` | Step-by-step fine-tuning guide |
| `provision_demo_env.ps1` | Provisioner and smoke-test runner |
| `provision_demo_env.py` | Python provisioner (used by the PS1 script) |
| `stage1_release_gate.py` | Stage 1 standalone script (fallback / smoke tests) |
| `stage2_rag_boundary.py` | Stage 2 standalone script (fallback / smoke tests) |
| `stage3_action_gate.py` | Stage 3 standalone script (fallback / smoke tests) |
| `data/` | Fixture files (tickets, RAG docs, agent scenarios) |
| `fallback/` | Screenshots / recordings for offline fallback |
| `install_plan.md` | Detailed installation and troubleshooting guide |
| `demo_plan.md` | Full demo script with speaker narration |


