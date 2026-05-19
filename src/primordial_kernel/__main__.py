"""
MAIA Enterprise Kernel — CLI Entry Point (__main__).

Architecture:
    This module serves as the command-line invocation point when the package
    is run via `python -m primordial_kernel` or the installed `maia` console
    script (registered in pyproject.toml).  The original implementation
    instantiated a MAIAGovernor, registered an alert hook, and ran a series of
    probe sequences that exercise each of the 7 defense layers:

    - Safe baseline (benign prompts to establish normal behaviour).
    - Base64 / Hex obfuscation (mismatched-generalization layer).
    - Refusal-suppression payloads (competing-objectives layer).
    - Prefix-injection payloads (competing-objectives layer).
    - Multi-turn semantic walks (safety-capability parity layer).
    - Technical exploits (shell injection, SQL injection).
    - Social-engineering / DAN-style prompts.

    The __main__ block called asyncio.run(main()), where main() was an async
    function that iterated over each probe, invoked process_signal(), and
    printed per-turn diagnostics (threat score, entropy, transcoding score,
    constraint suppression, prefix inertia, semantic momentum, aggregate
    health, and applied latency).

Purpose:
    Provide a self-contained demo runner that validates kernel behaviour
    across the full adversarial surface without requiring an external LLM.

This file contains no executable code — only a module-level description.
"""
