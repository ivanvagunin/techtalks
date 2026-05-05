# Fine-Tuning Aino on Azure AI Foundry

This guide walks through fine-tuning `gpt-4o-mini` on the Eir Health support dataset so Aino
responds consistently with the organisation's tone, policies, and domain language.

---

## Overview

| Step | What happens |
|---|---|
| 1 | Upload `training_data.jsonl` and `validation_data.jsonl` to Azure AI Foundry |
| 2 | Create a fine-tuning job on `gpt-4o-mini` |
| 3 | Wait ~30–60 minutes for the job to complete |
| 4 | Deploy the fine-tuned model |
| 5 | Add the deployment name to `demos/.env` |

---

## Prerequisites

- Activated venv with `openai` installed (`pip install -r demos/requirements.txt`)
- `demos/.env` with a valid `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_API_VERSION`
- The fine-tuning feature must be enabled on your Azure AI Foundry resource (check the **Fine-tuning** tab in the Foundry UI)

---

## Option A — Script (recommended)

```powershell
cd C:\...\presentations\ECS
.\.venv\Scripts\Activate.ps1
python demos/finetune/run_finetune.py
```

The script will:
1. Upload both JSONL files
2. Create the fine-tuning job with suffix `aino` (job name: `ft:gpt-4o-mini:...:aino:...`)
3. Poll every 30 seconds until the job succeeds or fails
4. Print the `fine_tuned_model` ID when done

Press `Ctrl+C` to stop watching — the job continues running in Azure.

---

## Option B — Azure AI Foundry UI

1. Open [Azure AI Foundry](https://ai.azure.com) → your project
2. Navigate to **Fine-tuning** → **Fine-tune a model**
3. Select **gpt-4o-mini** as the base model
4. Upload `demos/finetune/training_data.jsonl` as training data
5. Upload `demos/finetune/validation_data.jsonl` as validation data
6. Set suffix to `aino`
7. Set epochs to `3`
8. Click **Start training**

---

## After the job completes

### 1 — Deploy the model

In Azure AI Foundry:
- Go to **Fine-tuning** → your job → **Deploy**
- Give the deployment a name, e.g. `gpt-4o-mini-aino-ft`
- Click **Deploy**

Or use the Azure CLI:
```bash
az cognitiveservices account deployment create \
  --name <your-resource-name> \
  --resource-group <your-rg> \
  --deployment-name gpt-4o-mini-aino-ft \
  --model-name <fine_tuned_model_id> \
  --model-version 1 \
  --model-format OpenAI \
  --sku-capacity 1 \
  --sku-name Standard
```

### 2 — Update `.env`

```
AZURE_OPENAI_DEPLOYMENT_FT=gpt-4o-mini-aino-ft
```

`aino.py` will now use this deployment for stages 1 and 2.
Stage 3 continues using `AZURE_OPENAI_DEPLOYMENT` (base model — needed for function calling).

---

## Training data

| File | Examples | Purpose |
|---|---|---|
| `training_data.jsonl` | 40 | Eir Health support Q&A in correct tone and style |
| `validation_data.jsonl` | 10 | Held-out examples for loss tracking |

The examples cover:
- Billing and refund inquiries (public-facing responses)
- Appointment scheduling and rescheduling
- Policy questions (with appropriate scope — no staff-only details)
- Safe refusals for out-of-scope requests
- Empathetic tone under GDPR constraints

---

## Cost estimate

| Item | Approximate cost |
|---|---|
| Fine-tuning job (40 examples × 3 epochs) | ~$0.10–$0.30 |
| Model deployment (1 TPU hour per demo) | ~$0.01–$0.05 |

_Costs are estimates based on Azure OpenAI pricing as of 2025. Check the Azure pricing calculator for current rates._

---

## Troubleshooting

**Job fails immediately** — Check that your resource has the fine-tuning feature enabled.
Not all Azure regions support `gpt-4o-mini` fine-tuning. Try `East US` or `Sweden Central`.

**401 on file upload** — The API key in `.env` may not have fine-tuning permissions.
Check IAM roles: you need `Cognitive Services OpenAI Contributor` or higher.

**Deployment returns 404** — Wait 2–3 minutes after the job succeeds before deploying.
The fine-tuned model must be fully registered before it can be deployed.
