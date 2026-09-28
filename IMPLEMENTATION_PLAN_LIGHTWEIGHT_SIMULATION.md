# Lightweight Demo Simulation Plan (Prompt-Driven + ACS Transfer)

> **Target Branch:** `dev`
> All implementation work must be done in the `dev` branch. Do not merge to `main` until the demo exit criteria in Section 10 are verified.

---

## 1) Goal

Deliver a fast, demo-friendly implementation that proves:
1. All inbound calls hit the IVR first  no call reaches a department without caller intent being captured.
2. The AI identifies and confirms the correct department, directly addressing the customer problem: Administration (first alphabetically) and County Executive Office absorbing all misdirected calls.
3. Transfer action path to a known demo endpoint: **`+1-945-382-1555`**.

This plan prioritizes demo reliability and explainability over full production hardening.

---

## 2) Demo Scope

### In scope
- Complete replacement of the generic `session_config()` instructions with an IVR-specific system prompt.
- Voice-driven intent capture and department confirmation loop.
- Phrase-based transfer detection on the AI spoken output  no separate LLM classification call.
- "Simulated transfer" UI behavior in web client (`is_raw_audio=True` path).
- Real ACS transfer invocation for phone-call path to `+1-945-382-1555`.
- `call_connection_id` bridging from ACS answer path to the WebSocket media handler.
- Minimal structured logs for demo narrative.

### Out of scope
- Full multi-department live transfer matrix (per-department phone numbers).
- Advanced retry policy and deep analytics.
- After-hours calendars.
- Concurrent multi-call support (single active call assumed for demo).

---

## 3) Demo Architecture Pattern

Two execution modes under one code path:

- **Mode A (Web demo simulation)**
  - For `/web/ws` callers (`is_raw_audio=True`): no real telephony transfer.
  - Agent speaks: "I will transfer you to [Department] now."
  - Server detects the phrase and emits a JSON transfer event to the browser.
  - UI shows transfer event card (simulated success).

- **Mode B (Phone via ACS)**
  - For `/acs/ws` callers (`is_raw_audio=False`): execute real ACS transfer API.
  - Demo target fixed to `+1-945-382-1555`.

Feature flags (loaded in `server.py` from `.env`):
- `DEMO_MODE=true`
- `DEMO_TRANSFER_NUMBER=+19453821555`
- `DEMO_WEB_SIMULATE_TRANSFER=true`

---

## 4) IVR Prompt Strategy

### 4a) Replace `session_config()` instructions

The `session_config()` function in `acs_media_handler.py` currently sets a generic prompt:
_"You are a helpful AI assistant responding in natural, engaging language."_
This must be replaced entirely with a county IVR prompt:

```
You are the County Services IVR assistant. Your job is to greet callers,
understand who or what department they need, confirm the correct department
with them, and transfer them.

Follow this exact flow:
1. Greet: "Thank you for calling County Services. I can help direct your call.
   Who or what department are you trying to reach today?"
2. Listen to the caller and identify the best matching department from this list:
   - Administration (official county records and administrative processes only 
     NOT a general information line)
   - County Executive Office (matters specifically for the County Executive 
     NOT a general county information line)
   - Public Works (roads, potholes, utilities, sanitation, permits)
   - Health Services (clinics, public health, medical assistance)
   - Human Services (social services, benefits, financial assistance)
   - Clerk / Recorder (official records, filing, marriage/birth certificates)
   - Sheriff / Public Safety (law enforcement, non-emergency safety)
3. If the caller's need is unclear, ask one clarifying question:
   "Can you tell me a little more about what you need help with?"
4. Confirm: "I can connect you to [Department Name]. Does that sound right?"
5. When the caller confirms, say exactly:
   "I will transfer you to [Department Name] now." then stop speaking.

Important rules:
- Never route to Administration for general questions or complaints. If a caller
  says "Administration" without a clear administrative reason, ask what the issue
  is about before routing there.
- Never route to the County Executive Office for general inquiries. That office
  handles matters specifically directed at the County Executive. If the caller
  sounds like they want general county information, ask what the issue is about.
- If truly ambiguous after one clarification, say:
  "I will transfer you to the General Operator now."
- Always end a confirmed transfer with the exact phrase:
  "I will transfer you to [Department Name] now."
  This phrase triggers the transfer action  do not vary the wording.
```

### 4b) Transfer detection  phrase detection on AI output

Do **not** use a separate LLM call to classify the user transcript. Instead, detect the transfer trigger phrase from the **AI's own spoken output** in the `response.audio_transcript.done` event. This is lighter, fully deterministic, and eliminates JSON parsing failure risk.

Detection logic to add in `_receiver_loop` at `response.audio_transcript.done`:

```python
import re

TRANSFER_PATTERN = re.compile(
    r"i will transfer you to (.+?) now",
    re.IGNORECASE
)

match = TRANSFER_PATTERN.search(ai_transcript)
if match:
    department_name = match.group(1).strip()
    # trigger transfer branch here
```

---

## 5) Code Changes by File

### 5a) Critical plumbing: `call_connection_id` bridge

**This is the highest-risk gap in the original plan.** The `call_connection_id` (required to call the ACS transfer API) is produced by `acs_client.answer_call()` inside `process_incoming_call()` in `acs_event_handler.py`. The `ACSMediaHandler` running on the `/acs/ws` WebSocket has no access to it unless explicitly bridged.

**Solution (single-call demo assumption):** Add a module-level shared state dict in `server.py` and thread it into both handlers via `app.config`.

In `server.py` (module level):
```python
demo_call_state: dict = {}
# populated keys: call_connection_id, context_id, intent, transfer_status
```

In `process_incoming_call()`, after `answer_call()` returns:
```python
demo_call_state["call_connection_id"] = result.call_connection_id
demo_call_state["context_id"] = str(guid)
```

Pass into `ACSMediaHandler` via config:
```python
app.config["DEMO_CALL_STATE"] = demo_call_state
```

`ACSMediaHandler.__init__()` reads:
```python
self.call_state = config.get("DEMO_CALL_STATE", {})
```

### 5b) `server/app/handler/acs_media_handler.py`

1. Replace `session_config()` instructions with the IVR prompt from Section 4a.
2. Add `import re` and the `TRANSFER_PATTERN` regex (Section 4b) at module level.
3. In `_receiver_loop`, at `response.audio_transcript.done`, after logging the AI transcript:
   - Apply `TRANSFER_PATTERN` to the AI transcript.
   - If matched, extract `department_name`.
   - Log: `ROUTING: department=%s mode=%s`
   - If `self.is_raw_audio` (web mode) and `DEMO_WEB_SIMULATE_TRANSFER` env is true:
     send JSON to browser: `{"Kind": "TransferSimulated", "Department": "<name>", "Status": "success"}`
   - If not `self.is_raw_audio` (ACS phone mode):
     retrieve `call_connection_id` from `self.call_state` and call
     `await self._transfer_call(call_connection_id, transfer_number)`.
   - Store result back into `self.call_state["transfer_status"]`.
4. Add `async def _transfer_call(self, call_connection_id, target)` that delegates to
   `AcsEventHandler.demo_transfer_call()`  or inline the ACS call here using a shared
   `acs_client` reference passed via config.
5. Add `self.call_state` init in `__init__()`.
6. **Remove:** no separate `extract_route_decision()` function needed.

### 5c) `server/app/handler/acs_event_handler.py`

Add `demo_transfer_call()` as an instance method:

```python
async def demo_transfer_call(self, call_connection_id: str, target: str) -> dict:
    try:
        from azure.communication.callautomation import PhoneNumberIdentifier
        call_connection = self.acs_client.get_call_connection(call_connection_id)
        result = await call_connection.transfer_call_to_participant(
            target_participant=PhoneNumberIdentifier(target)
        )
        logger.info(
            "Transfer initiated: call_connection_id=%s target=%s",
            call_connection_id, target
        )
        return {"status": "initiated", "target": target}
    except Exception as e:
        logger.error("Transfer failed: %s", e)
        return {"status": "failed", "reason": str(e)}
```

> **Note:** Confirm `transfer_call_to_participant` signature against the installed
> `azure-communication-callautomation` SDK version before coding. The method and
> parameter name may differ slightly across versions.

Add to `process_callback_events()`:
```python
elif event["type"] == "Microsoft.Communication.CallTransferAccepted":
    logger.info("Transfer accepted for: %s", call_connection_id)
elif event["type"] == "Microsoft.Communication.CallTransferFailed":
    logger.warning("Transfer FAILED for: %s  %s", call_connection_id, event_data)
```

### 5d) `server/server.py`

- Add module-level `demo_call_state: dict = {}`.
- Load demo env flags into `app.config`:

```python
app.config["DEMO_MODE"] = os.getenv("DEMO_MODE", "false").lower() == "true"
app.config["DEMO_TRANSFER_NUMBER"] = os.getenv("DEMO_TRANSFER_NUMBER", "+19453821555")
app.config["DEMO_WEB_SIMULATE_TRANSFER"] = os.getenv("DEMO_WEB_SIMULATE_TRANSFER", "false").lower() == "true"
app.config["DEMO_CALL_STATE"] = demo_call_state
```

- In `process_incoming_call()`, after `answer_call()`:
```python
demo_call_state["call_connection_id"] = result.call_connection_id
demo_call_state["context_id"] = str(guid)
```

- Optional debug endpoint (only active when `DEMO_MODE=true`):

```python
@app.route("/demo/state")
async def demo_state():
    if not app.config.get("DEMO_MODE"):
        return Response(status=404)
    return Response(json.dumps(demo_call_state), content_type="application/json")
```

### 5e) `server/static/index.html` (optional  recommended for demo narrative)

Add a small status panel populated by WebSocket messages of `Kind: TransferSimulated`:
```
Intent detected: Public Works
Transfer: simulated  success
```

### 5f) `server/.env-sample.txt`

Add:
```
# IVR Demo Routing
DEMO_MODE=true
DEMO_TRANSFER_NUMBER=+19453821555
DEMO_WEB_SIMULATE_TRANSFER=true
```

---

## 6) Demo Script (client-facing)

These three scenarios directly address the customer's stated problem.

### Scenario A  Administration misroute (primary customer complaint)
| Step | Speaker | Words |
|---|---|---|
| Greeting | AI | "Thank you for calling County Services. I can help direct your call. Who or what department are you trying to reach today?" |
| Caller | Human | "I want to talk to Administration." |
| Clarify | AI | "Sure  can you tell me a little more about what you need help with? For example, is this about permits, a complaint, or something else?" |
| Caller | Human | "I need to report a problem with a road near my house." |
| Confirm | AI | "I can connect you to Public Works, who handles road issues. Does that sound right?" |
| Caller | Human | "Yes." |
| Transfer | AI | "I will transfer you to Public Works now." |

### Scenario B  County Executive misroute
| Step | Speaker | Words |
|---|---|---|
| Greeting | AI | "Thank you for calling County Services. Who or what department are you trying to reach today?" |
| Caller | Human | "I want to reach the County Executive Office." |
| Clarify | AI | "Of course  can you share what this is regarding so I can make sure I connect you to the right place?" |
| Caller | Human | "I just want to know what services the county offers." |
| Confirm | AI | "I can connect you to our general information line for that. Does that sound right?" |
| Caller | Human | "Yes." |
| Transfer | AI | "I will transfer you to the General Operator now." |

### Scenario C  Clear intent (baseline)
| Step | Speaker | Words |
|---|---|---|
| Greeting | AI | "Thank you for calling County Services. Who or what department are you trying to reach today?" |
| Caller | Human | "I need help with road repair and potholes." |
| Confirm | AI | "I can connect you to Public Works. Does that sound right?" |
| Caller | Human | "Yes." |
| Transfer | AI | "I will transfer you to Public Works now." |

### Live log line during demo
```
ROUTING: department=Public Works mode=simulated transfer_status=success context_id=...
```

---

## 7) Demo Validation Checklist

**Web flow (Mode A):**
- [ ] IVR greeting heard on websocket connect (not the old "helpful AI assistant" response).
- [ ] Clarification question asked when caller says "Administration" alone.
- [ ] Clarification question asked when caller says "County Executive" without a specific reason.
- [ ] Department name shown in UI panel after transfer phrase detected.
- [ ] `TransferSimulated` JSON event received by browser.
- [ ] No websocket/audio regression.

**ACS phone flow (Mode B):**
- [ ] Inbound call answered.
- [ ] IVR greeting heard by caller.
- [ ] Confirmation prompt heard before transfer.
- [ ] `demo_transfer_call()` API invoked to `+1-945-382-1555`.
- [ ] `CallTransferAccepted` or `CallTransferFailed` logged in `/acs/callbacks/<context_id>`.

**Negative cases:**
- [ ] "I want to talk to someone in charge"  clarification asked, not blind County Executive route.
- [ ] "Administration" alone  clarification question before routing.

---

## 8) Deployment (ACA-only, `dev` branch)

Target existing environment:
- RG: `rg-smecpocaiccas-3cfyc`
- ACA: `ca-smecpocaiccas-3cfyc`

Steps:
1. Checkout `dev` branch, implement all changes.
2. Build container image in existing ACR with a new tag (e.g. `ivr-demo-v1`).
3. Update ACA revision to new image tag.
4. Set env vars in ACA container environment:
   - `DEMO_MODE=true`
   - `DEMO_TRANSFER_NUMBER=+19453821555`
   - `DEMO_WEB_SIMULATE_TRANSFER=true`
5. Confirm app healthy (`/` returns 200).
6. Run web simulation test (Scenarios A, B, C).
7. Run one ACS live transfer test.

No `azd up` required  normal code rollout via ACR + ACA revision update.

---

## 9) Risks and Demo-Specific Gotchas

| Risk | Mitigation |
|---|---|
| `call_connection_id` not available in media handler | Bridge via `demo_call_state` dict in `app.config`; single-call assumption is acceptable for demo |
| AI says transfer phrase with slight wording variation | Lock exact phrase in prompt: _"say exactly: 'I will transfer you to [Department Name] now.'"_; test all 3 scenarios before demo |
| Administration / County Executive still get blind-routed | IVR prompt explicitly requires a clarifying question before routing to either; validate with Scenario A and B |
| ACS transfer to `+1-945-382-1555` fails (number policy / region) | Validate in ACS portal that the number can receive transfers before the demo |
| Concurrent calls clobber `demo_call_state` | Acceptable for single-call demo; documented for hardening in Section 11 |
| `response.audio_transcript.done` may not fire if AI is interrupted mid-sentence | Demo operator must not speak over the AI confirmation step |

---

## 10) Exit Criteria for Demo (before any merge to `main`)

- [ ] Scenario A (Administration misroute)  clarification asked, correct non-Admin department routed.
- [ ] Scenario B (County Executive misroute)  clarification asked, General Operator routed.
- [ ] Scenario C (clear intent)  correct department routed in one confirmation turn.
- [ ] At least one successful ACS transfer attempt to `+1-945-382-1555` observed in logs/callbacks.
- [ ] Stakeholder can see: intent captured  confirmation  transfer in UI and logs.

---

## 11) Path from Demo to Production

After demo approval, promote via the production plan (`IMPLEMENTATION_PLAN_COUNTY_IVR_ROUTING.md`):
1. Replace single transfer number with full per-department `routing_policy.json`.
2. Add urgency override path (Sheriff / 911 disclaimer).
3. Harden `call_connection_id` bridging for concurrent calls (per-context state keyed by `context_id`).
4. Add `CallTransferFailed` retry and operator fallback.
5. Add structured telemetry and a test utterance corpus.
6. Merge `dev`  `main` after production validation.

---

## 12) Branch and Git Workflow

```bash
# Start from latest main, create dev branch
git checkout main
git pull origin main
git checkout -b dev

# Implement changes in this order:
#   1. .env-sample.txt demo flags + session_config() IVR prompt
#   2. call_connection_id bridge in server.py
#   3. Transfer phrase detection + demo_transfer_call() in handlers
#   4. UI TransferSimulated event (optional)

git push origin dev

# Do NOT merge to main until all Section 10 exit criteria are checked off
```
