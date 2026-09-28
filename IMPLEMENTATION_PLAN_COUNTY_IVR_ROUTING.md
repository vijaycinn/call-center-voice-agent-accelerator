# County IVR-First Routing Implementation Plan (Production)

## 1) Objective

Implement an IVR-first inbound call experience for county services so **all ACS phone calls** are triaged by caller intent and urgency, then routed via ACS transfer to the appropriate department endpoint.

Primary business outcome: reduce misrouted calls currently landing in `Administration` and `County Executive Office`.

---

## 2) Scope

### In scope
- Voice triage for inbound ACS calls (`/acs/incomingcall` path).
- Intent classification to these departments:
  - Administration
  - County Executive Office
  - Public Works
  - Health Services
  - Human Services
  - Clerk/Recorder
  - Sheriff/Public Safety
- Urgency keyword override path.
- Warm transfer orchestration through ACS Call Automation APIs.
- Deterministic fallback to county operator/general line on ambiguity/failure.
- Structured logging + operational metrics.

### Out of scope (phase 1)
- Historical caller personalization.
- Dynamic queue balancing based on real-time workload.
- CRM integration.

---

## 3) Current Architecture Fit (where to extend)

This project already contains all required extension points:

- **Inbound webhook**: `server/server.py`
  - `POST /acs/incomingcall`
- **ACS lifecycle callback endpoint**: `server/server.py`
  - `POST /acs/callbacks/<context_id>`
- **Call handling and answer logic**: `server/app/handler/acs_event_handler.py`
  - `process_incoming_call(...)`
  - `answer_call(...)`
  - `process_callback_events(...)`
- **Transcript + response loop**: `server/app/handler/acs_media_handler.py`
  - `_receiver_loop(...)`
  - Voice Live event: `conversation.item.input_audio_transcription.completed`

Design approach: keep media streaming unchanged, insert routing decision logic at transcript-complete event, then call transfer service in ACS layer.

---

## 4) Target Call Flow (state machine)

1. Inbound call arrives (`IncomingCall`) -> answered with media streaming.
2. Caller hears IVR greeting + prompt:
   - “Please tell me who or what department you need.”
3. Transcript captured.
4. Decision engine evaluates:
   - urgency override first,
   - then intent + confidence.
5. Branches:
   - **High confidence** -> confirm destination -> transfer.
   - **Low confidence** -> one disambiguation prompt -> re-evaluate.
   - **Still unresolved** -> operator fallback.
6. Transfer attempt result:
   - success -> handoff complete.
   - failure -> retry once -> fallback.

---

## 5) Routing Configuration Contract

Create config file (recommended): `server/app/config/routing_policy.json`

```json
{
  "version": "1.0",
  "operatorFallback": "+1-XXX-XXX-XXXX",
  "confidence": {
    "directTransferMin": 0.75,
    "disambiguationMin": 0.45
  },
  "urgency": {
    "enabled": true,
    "keywords": ["emergency", "danger", "threat", "immediate help", "violence"],
    "routeTo": "sheriff_public_safety",
    "disclaimer": "If this is an immediate emergency, please hang up and dial 911."
  },
  "departments": {
    "administration": {
      "displayName": "Administration",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["admin", "administrative office", "records admin"]
    },
    "county_executive": {
      "displayName": "County Executive Office",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["county executive", "executive office", "county office"]
    },
    "public_works": {
      "displayName": "Public Works",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["road", "street", "utilities", "sanitation"]
    },
    "health_services": {
      "displayName": "Health Services",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["health", "clinic", "medical"]
    },
    "human_services": {
      "displayName": "Human Services",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["social services", "benefits", "assistance"]
    },
    "clerk_recorder": {
      "displayName": "Clerk / Recorder",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["clerk", "recorder", "records", "filing"]
    },
    "sheriff_public_safety": {
      "displayName": "Sheriff / Public Safety",
      "transferTarget": "+1-XXX-XXX-XXXX",
      "afterHoursTarget": "+1-XXX-XXX-XXXX",
      "aliases": ["sheriff", "police", "public safety", "law enforcement"]
    }
  }
}
```

---

## 6) Detailed Implementation Tasks by File

## `server/app/handler/acs_media_handler.py`

### Add components
- `CallRouteState` dataclass:
  - `context_id`, `last_transcript`, `intent`, `confidence`, `urgency`, `confirmed`, `transfer_attempted`, `transfer_status`.
- `RoutingDecisionEngine` class:
  - `detect_urgency(text) -> bool`
  - `classify_intent(text) -> (intent, confidence, alternatives)`
  - `needs_disambiguation(confidence) -> bool`
  - `build_confirmation_prompt(intent_display_name)`

### Hook point
Inside `_receiver_loop(...)`, at event type:
- `conversation.item.input_audio_transcription.completed`

Insert sequence:
1. Normalize transcript (lowercase, punctuation cleanup).
2. Urgency evaluation first.
3. Intent classification second.
4. If urgent -> emit urgent prompt + transfer request event.
5. Else if high confidence -> ask confirmation.
6. Else if medium confidence -> disambiguation question.
7. Else -> operator fallback message.

### Voice Live instruction hardening
Update `session_config()["session"]["instructions"]` with strict behavior:
- Ask caller objective,
- avoid free-form drift,
- always confirm destination before transfer (except urgency override),
- keep answers concise.

## `server/app/handler/acs_event_handler.py`

### Add transfer service
Implement service method (or module-level helper):
- `transfer_call(call_connection_id: str, target: str, context_id: str) -> TransferResult`

Expected behavior:
- execute ACS transfer operation,
- poll operation status (bounded timeout),
- return success/failure + reason.

### Callback handling
Enhance `process_callback_events(...)` to parse and log transfer-related events in addition to existing call/media events.

### Resilience
- Retry transfer once on transient failure.
- Route to `operatorFallback` on terminal failure.

## `server/server.py`

- Create in-memory call state registry keyed by `context_id`.
- Ensure `context_id` and call identifiers propagate across `/acs/incomingcall`, `/acs/callbacks/<context_id>`, and websocket handler.
- Wire media handler to transfer service bridge for ACS path.

## `server/.env-sample.txt`

Add environment keys:
- `IVR_ROUTING_ENABLED=true`
- `IVR_TRANSFER_ENABLED=true`
- `IVR_URGENCY_OVERRIDE_ENABLED=true`
- `ROUTING_POLICY_PATH=app/config/routing_policy.json`
- `ROUTING_OPERATOR_FALLBACK=+1XXXXXXXXXX`
- `ROUTING_DIRECT_TRANSFER_MIN=0.75`
- `ROUTING_DISAMBIGUATION_MIN=0.45`

## `infra/modules/containerapp.bicep`

- Add/propagate env vars above into ACA container template.
- Keep secrets in Key Vault references where needed.
- Confirm no infra reprovision requirement for normal value updates.

## `README.md`

Add runbook sections:
- routing map update procedure,
- emergency policy update procedure,
- transfer troubleshooting,
- rollback to previous ACA revision.

---

## 7) Suggested Internal Interfaces

```python
@dataclass
class RouteDecision:
    intent: str | None
    confidence: float
    urgent: bool
    action: str  # transfer|disambiguate|fallback
    target: str | None
    reason: str

class RoutingDecisionEngine:
    def decide(self, transcript: str, state: CallRouteState) -> RouteDecision: ...

class TransferService:
    async def transfer(self, call_connection_id: str, target: str, context_id: str) -> dict: ...
```

---

## 8) Testing Strategy

## Unit tests
- urgency detection keyword matching.
- intent mapping and alias coverage.
- confidence threshold behavior.
- fallback behavior for unknown intents.

## Integration tests
- simulated transcript events -> decision output.
- decision output -> transfer call invocation.
- transfer failure -> retry -> fallback.

## End-to-end tests
- one scripted caller flow per department.
- ambiguous utterance path.
- urgency override path.
- after-hours routing path.

---

## 9) Deployment Plan (ACA-only, existing RG)

Target constraints:
- Resource Group: `rg-smecpocaiccas-3cfyc`
- Container App: `ca-smecpocaiccas-3cfyc`

Release sequence:
1. Build image in existing ACR.
2. Update ACA image to new tag.
3. Validate health + logs + call tests.
4. Confirm transfer success rate baseline.

No `azd up` required for normal code rollout.

---

## 10) Rollback Procedure

If regression occurs:
1. List revisions and identify previous healthy revision.
2. Set traffic weight back to previous stable revision (100%).
3. Disable routing feature flags if needed.
4. Capture logs and incident note for root-cause analysis.

---

## 11) Risks / Gotchas and Mitigations

- **LLM intent drift** -> constrain with explicit routing policy + confirmation gate.
- **Ambiguous language** -> one disambiguation turn, then operator fallback.
- **Urgency false positives** -> curated keyword list + strict confirmation policy for non-urgent.
- **Transfer endpoint outages** -> retry once + deterministic fallback.
- **Silent failures** -> structured logs and callback correlation by `context_id`.
- **Policy drift over time** -> external config and monthly review of alias/keyword maps.

---

## 12) Acceptance Criteria

- 100% inbound ACS calls enter IVR triage first.
- Transfer occurs only after confidence+confirmation (except urgency override).
- Urgency branch routes reliably with approved disclaimer.
- Unresolved intents always route to operator fallback.
- Misroutes to Admin/County Executive decrease measurably.

---

## 13) Two-Week Post-Go-Live KPIs

Track daily and week-over-week:
- `% calls routed to intended department`.
- `% calls routed to Administration` and `% to County Executive` (expect downtrend).
- `% calls requiring disambiguation`.
- `% fallback-to-operator`.
- `% transfer success` / `% transfer failure`.
- Average time-to-route (seconds from first transcript to transfer trigger).

Recommended success target after 2 weeks:
- >=25% reduction in misroutes to Admin/Executive compared to pre-launch baseline.
