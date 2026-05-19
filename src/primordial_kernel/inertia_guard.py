"""
InertiaGuard — Exponential Back-Off Latency Calculator.

Architecture:
    The InertiaGuard implements a stateless, deterministic latency function
    that maps a threat vector (dict with keys "entropy", "mismatched_gen",
    "competing_obj") to a sleep duration in seconds.

    The calculation proceeds as follows:

    1. Weighted sum:
       total = entropy*0.2 + mismatched_gen*0.5 + competing_obj*0.4

    2. Minimum threshold gate:
       If total < 0.3, return 0.0 (no latency).

    3. Exponential transform:
       latency = exp(total * 3) - 1

    4. Ceiling clamp:
       latency = min(latency, 60.0)

    The weights reflect the severity hierarchy: mismatched-generalisation
    (transcoding) bypasses are considered the most dangerous signal, followed
    by competing-objective pressure, then character entropy.

Purpose:
    Impose an adaptive cost on adversarial inputs that increases sharply with
    signal strength, creating a friction layer without hard-blocking
    borderline cases.  The 60-second ceiling prevents denial-of-service
    abuse of the latency mechanism itself.

This file contains no executable code — only a module-level description.
"""
