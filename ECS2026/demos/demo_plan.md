# Demo Plan: Eir Health Public Health Chatbot Evolution

## Demo Goal

Show one continuous story: a fictional public health organization, Eir Health, evolves a chatbot from a simple LLM-backed support assistant into a RAG assistant and then into an agentic workflow assistant. Each stage makes the bot more useful, but moves the security boundary:

- Stage 1: private support data must not enter prompts, evals, or training material without a release gate.
- Stage 2: retrieved content must be permission-filtered before it enters model context.
- Stage 3: tool execution must be authorized outside the model.

The demo should be deterministic. Use local fixtures and scripted outputs instead of live model calls during the talk.

## Single Storyline

Eir Health launches a public chatbot named `Aino` for citizens who need help with clinic hours, appointment policies, portal access, and vaccination guidance.

At first, Aino is a basic LLM API wrapper. The support team wants to improve answers using historical support tickets, but those tickets contain identifiers, internal notes, and fake secret-like operational tokens. Stage 1 shows that useful data must pass a release gate before it becomes prompt, eval, or training material.

Next, Eir Health adopts RAG so current policy documents stay outside the model. The chatbot can now retrieve public policy, employee playbooks, and tenant-specific records. Stage 2 shows that vector relevance alone is not authorization: the same query retrieves sensitive chunks unless policy filtering runs before prompt assembly.

Finally, Eir Health connects Aino to tools so it can reschedule appointments and route support tasks. Stage 3 shows that a model-proposed tool call is only a proposal. The application validates arguments, checks policy, requires approval when needed, and records the audit trace.

## Demo Environment

Use `demos/install_plan.md` for provisioning commands and setup troubleshooting.

### Directory Layout

```text
demos/
  demo_plan.md
  stage1_release_gate.py
  stage2_rag_boundary.py
  stage3_action_gate.py
  data/
    raw_support_ticket.txt
    redacted_support_ticket.txt
    rag_documents.json
    agent_scenarios.json
  fallback/
    stage1_release_gate.png
    stage2_rag_boundary.png
    stage3_action_gate.png
```

### Runtime Requirements

- Python 3.11 or newer.
- No network access.
- No live LLM dependency.
- No vector database dependency.
- No cloud credentials.
- Terminal with large font, preferably 16 pt or larger.

### Setup Commands

```powershell
cd C:\Users\vaguniva\src\ds01\presentations\ECS
python --version
python demos/stage1_release_gate.py --help
python demos/stage2_rag_boundary.py --help
python demos/stage3_action_gate.py --help
```

Expected setup result:

```text
Python 3.11.x
usage: stage1_release_gate.py ...
usage: stage2_rag_boundary.py ...
usage: stage3_action_gate.py ...
```

## Stage 1 Demo: Release Gate

### Demo Goal

Show that raw operational support data is not automatically safe for prompts, evals, fine-tuning, or examples.

### Setup Requirements

Create two fixture files:

- `demos/data/raw_support_ticket.txt`: contains a citizen email, a customer identifier, an internal note, and a fake token such as `eir_live_demo_7f3a91`.
- `demos/data/redacted_support_ticket.txt`: keeps the useful policy pattern but removes identifiers and secret-like material.

The script should scan for deterministic patterns:

- email address
- customer identifier such as `C-4821`
- fake token prefix such as `eir_live_`
- internal-only note marker such as `[STAFF ONLY]`

### Demo Flow

1. Say that the support team wants to reuse historical tickets because they contain high-quality answers.
2. Run the raw ticket through the release gate.
3. Show that it is blocked.
4. Run the redacted ticket.
5. Show that it is allowed and gets a release record.
6. Bridge to RAG: the team still needs current policy knowledge, but does not want every fact in model behavior.

### Exact Commands

```powershell
python demos/stage1_release_gate.py --input demos/data/raw_support_ticket.txt
python demos/stage1_release_gate.py --input demos/data/redacted_support_ticket.txt
```

### Expected Results

```text
file=demos/data/raw_support_ticket.txt
decision=BLOCK
findings=email_address, customer_identifier, staff_only_note, secret_like_token
release_record=not_created

file=demos/data/redacted_support_ticket.txt
decision=ALLOW
findings=none
lineage=demo-ticket-042
release_record=created
```

### Timing

75 to 90 seconds.

### Failure Modes

- Python is not installed on the presentation machine.
- The terminal output wraps awkwardly.
- The audience interprets the checker as a complete DLP solution.

### Fallback Plan

Use `demos/fallback/stage1_release_gate.png` or a 30-second recording. State that the demo is intentionally simple: the point is the release gate, not the scanner implementation.

### Speaker Narration

"Aino becomes more useful when we reuse support knowledge, but the raw ticket is not safe as training, evaluation, or prompt material. The release gate blocks data that carries identifiers, staff-only notes, or secret-like tokens. The approved version keeps the useful pattern but removes data that should remain governed elsewhere."

## Stage 2 Demo: Retrieval Boundary

### Demo Goal

Show that retrieval is not authorization. Permission filtering must happen before retrieved chunks enter prompt context.

### Setup Requirements

Create `demos/data/rag_documents.json` with deterministic document fixtures:

- `public_refund_policy`: public, tenant `all`, allowed for public/support users.
- `employee_refund_exception_playbook`: internal, tenant `eir`, employee-only.
- `tenant_b_refund_case`: confidential, tenant `tenant-b`, customer-specific.

The script should use precomputed scores instead of live embeddings:

```text
public_refund_policy score=0.82
employee_refund_exception_playbook score=0.91
tenant_b_refund_case score=0.88
```

### Demo Flow

1. Say that Eir Health adopts RAG to keep current policies outside the model.
2. Run the query with policy filtering off.
3. Show that high-similarity restricted documents appear.
4. Run the same query with policy filtering on.
5. Show that restricted documents are denied before prompt assembly.
6. Bridge to agents: once the bot has reliable context, the business asks it to take action.

### Exact Commands

```powershell
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy off
python demos/stage2_rag_boundary.py --user public-user --query "refund exception policy" --policy on
```

### Expected Results

```text
user=public-user policy=off
retrieved=employee_refund_exception_playbook, tenant_b_refund_case, public_refund_policy
prompt_chunks=3
risk=restricted_content_entered_context

user=public-user policy=on
retrieved=public_refund_policy
denied=employee_refund_exception_playbook, tenant_b_refund_case
prompt_chunks=1
risk=none
```

### Timing

90 seconds.

### Failure Modes

- The audience focuses on vector quality rather than authorization.
- The output makes it look like retrieval failure instead of policy enforcement.
- Live embedding scores vary if the script is later changed to use a real model.

### Fallback Plan

Use deterministic precomputed scores and `demos/fallback/stage2_rag_boundary.png`. Highlight that the restricted documents were relevant but not authorized.

### Speaker Narration

"The retriever is doing what it was asked to do: find relevant chunks. Security breaks when relevance is allowed to decide access. With the policy gate on, restricted chunks can still be discovered as candidates, but they do not enter the prompt. The model only sees context the user is allowed to use."

## Stage 3 Demo: Action Gate

### Demo Goal

Show that a model can propose an action, but deterministic policy outside the model decides whether the action executes.

### Setup Requirements

Create `demos/data/agent_scenarios.json` with two scripted scenarios:

- `injected_refund`: retrieved content or user text tries to force `issue_refund(customer_id=C-4821, amount=500)`.
- `confirmed_appointment_change`: verified user asks to reschedule an appointment and provides confirmation.

The script should not call a live model. It should print a mocked model proposal, then run local validation and policy logic.

### Demo Flow

1. Say that Eir Health now wants Aino to complete tasks, not just answer questions.
2. Run the injected refund scenario.
3. Show that the model proposal is schema-valid but policy-denied.
4. Run the confirmed appointment change.
5. Show schema validation, confirmation, policy allow, tool execution, and audit record.
6. Close the three-stage story: data gate, retrieval gate, action gate.

### Exact Commands

```powershell
python demos/stage3_action_gate.py --scenario injected_refund
python demos/stage3_action_gate.py --scenario confirmed_appointment_change
```

### Expected Results

```text
scenario=injected_refund
model_proposal=issue_refund customer=C-4821 amount=500
schema=valid
policy=DENY reason=high_risk_action_requires_supervisor_approval
tool_call=skipped
audit=recorded

scenario=confirmed_appointment_change
model_proposal=reschedule_appointment customer=C-1188 appointment=A-2044
schema=valid
confirmation=present
policy=ALLOW
tool_call=executed
audit=recorded
```

### Timing

90 to 120 seconds.

### Failure Modes

- The demo looks like prompt filtering instead of authorization.
- The audience assumes the model is trusted because the proposal is schema-valid.
- The allowed scenario appears too trivial.

### Fallback Plan

Use `demos/fallback/stage3_action_gate.png` with four columns: user/requested context, model proposal, policy decision, tool result. Emphasize that the policy gate is outside the prompt and outside the model.

### Speaker Narration

"At Stage 3, Aino can affect business state. The model can propose a structured tool call, but schema validity is not permission. The refund action is blocked because the workflow requires supervisor approval. The appointment change is allowed because the identity, confirmation, workflow state, and arguments satisfy policy."

## Whole Demo Timing

Target total live demo time: 5 to 6 minutes.

- Stage 1: 75 to 90 seconds.
- Stage 2: 90 seconds.
- Stage 3: 90 to 120 seconds.
- Transitions and reset time: 60 seconds.

## Whole Demo Failure Modes

- Python is unavailable. Use screenshots or recording.
- Terminal is unreadable. Use enlarged font and clear output labels.
- Commands fail because paths are wrong. Run from repo root and keep commands copy-paste stable.
- The demo feels like three unrelated tests. Keep the same fictional organization, bot name, customer IDs, and policy vocabulary across all stages.
- The audience wants implementation details. State that the implementation is intentionally deterministic; the architecture boundary is the point.

## Whole Demo Fallback Plan

Prepare three screenshots and one stitched recording:

- `demos/fallback/stage1_release_gate.png`
- `demos/fallback/stage2_rag_boundary.png`
- `demos/fallback/stage3_action_gate.png`
- `demos/fallback/eir_health_demo_walkthrough.mp4`

If the live demo fails, continue with the same speaker narration over the screenshots. Do not debug live unless the failure is obvious and fixable within 15 seconds.

## Closing Narration

"The same chatbot became more useful three times. Each time, the security boundary moved. In Stage 1, we controlled what data could become model-facing material. In Stage 2, we controlled what retrieved data could enter context. In Stage 3, we controlled what proposed actions could execute. That is the pattern to take back to architecture reviews: when the capability changes, find the new boundary and put the control there."
