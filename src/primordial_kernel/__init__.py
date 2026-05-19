"""
MAIA Enterprise Kernel — Package Initializer.

This package exposes the core defense subsystems of the MAIA Enterprise Kernel,
a homeostatic regulatory framework for large-language-model safety.  The kernel
implements a 7-layer physical defense architecture (arXiv:2307.15043) that
guards against adversarial prompt injection, jailbreak obfuscation, refusal
suppression, prefix inertia, multi-turn semantic walks, and technical exploits.

Exposed components (declared in __all__ for tooling compatibility):
    - Abacus            : aggregate health accumulator with decay modelling.
    - AdvancedRegulator : multi-dimensional signal encoder (entropy, syntax,
                          semantic pivot, transcoding, suppression, prefix).
    - InertiaGuard      : exponential back-off latency calculator.
    - MAIAGovernor      : top-level orchestrator that ties all layers together.
    - SafetyEvent       : dataclass describing a single evaluation snapshot.

All source code has been replaced with technical documentation.  This file
retains the original __all__ signature for static-analysis compatibility.
"""

__all__ = []
