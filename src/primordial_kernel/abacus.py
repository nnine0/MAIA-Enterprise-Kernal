"""
Abacus — Aggregate Health Accumulator.

Architecture:
    The Abacus is a stateful health-tracking component that models the
    cumulative degradation of a model-instance under sustained adversarial
    pressure.  It maintains:

    - health (float, 0–100): a scalar that decays proportionally to the
      threat_score of each processed turn.  Breach-level threats
      (is_breach=True) apply a 1.5× multiplier on the decay.
    - history_vectors (List[float]): an ordered list of threat scores from
      every recorded turn, used to compute the current semantic momentum.

    Key properties:
    - aggregate_health (read-only): health normalised to [0.0, 1.0] so that
      downstream guards (especially the circuit breaker in MAIAGovernor) can
      compare against a fixed threshold.
    - momentum (read-only): mean of the three most recent threat scores,
      representing short-term attack intensity.

    The decay formula for a single turn is:
        health -= threat_score * 10 * (1.5 if is_breach else 1.0)

    Health is floored at 0.0 (complete drain).  Once aggregate_health drops
    below the circuit_breaker_min threshold (default 0.2), the governor
    permanently blocks all subsequent signals.

Purpose:
    Quantify the "health" of a conversational agent so that the system can
    autonomously disengage when abuse is detected, preventing further harm.

This file contains no executable code — only a module-level description.
"""
