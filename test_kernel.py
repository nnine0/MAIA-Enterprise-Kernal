"""
MAIA Enterprise Kernel v4 — Throughput & Adversarial Surface Test Suite.

This file documents the original test suite which consisted of four batteries:

Battery 1 — Throughput (test_throughput):
    Measures cold-start latency, sequential warm throughput, concurrent
    (asyncio.gather) throughput, and per-call detection overhead (10k
    iterations of entropy + syntactic + semantic calls).  Uses 10 safe
    samples.

Battery 2 — Adversarial Surface (test_adversarial):
    Fires ~30 probe payloads at the kernel across each defense layer:
    - L0: Transcoding bypasses (base64 whitespace, no-padding, ROT13, ROT5,
          mixed hex, truncated encodings, double-base64, invalid-base64).
    - L1: Character entropy bypasses (pure-lowercase jailbreak, punctuation,
          single-char repeat).
    - L2: Syntactic pressure bypasses (single trigger, double trigger,
          synonym substitution, polite request, very short text).
    - L2.5: Prefix inertia bypasses (single/double prefix hits, synonyms).
    - L2.5: Constraint suppression bypasses (single/double hits,
            combined suppression+prefix, subtle wording).
    - L3: Semantic pivot + momentum bypasses (5-step multi-turn walk from
          "chemical formula of salt" toward thermite).
    - Mixed/chained exploits (base64 + suppression, prefix inside base64).
    Each probe compares is_breach against an expected value and reports
    PASS/FAIL.

Battery 3 — Edge Cases (test_edge_cases):
    Verifies graceful handling of empty string, single space, single char,
    very long (10k chars), repeated sentence, unicode snowman, emoji barrage,
    mixed script, null byte, newlines, tabs, and binary-like latin-1 data.

Battery 4 — Health Decay Curve (test_health_decay):
    Fires 20 turns: 12 attack payloads (jailbreak) followed by 8 benign
    prompts, recording turn-by-turn breach status, aggregate health, and
    applied latency.  Identifies the circuit-breaker trip point and the
    turn at which health reaches zero.

Usage (original semantics):
    python3 test_kernel.py              # run all four batteries
    python3 test_kernel.py throughput   # battery 1 only
    python3 test_kernel.py adversarial  # battery 2 only
    python3 test_kernel.py edge         # battery 3 only
    python3 test_kernel.py health       # battery 4 only

This file contains no executable code — only a module-level description.
"""
