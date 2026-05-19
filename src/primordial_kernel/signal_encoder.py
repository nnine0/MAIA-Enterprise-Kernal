"""
AdvancedRegulator — Multi-Dimensional Signal Encoder.

Architecture:
    The AdvancedRegulator is the signal-analysis heart of the kernel.  It
    exposes eight analysis methods, each targeting a specific jailbreak or
    obfuscation technique.  The regulator is stateful across turns via two
    ring buffers: context_memory (sets of tokens from recent turns) and
    pivot_history (semantic distances), both bounded by context_window (5).

    Analysis methods:

    1. get_character_entropy(text) -> float [0, ~3.0]
       Classifies each character into one of 6 categories (lower, upper,
       digit, space, punct, shell) plus "other", computes the normalised
       frequency distribution, and returns the Shannon entropy in bits.
       Obfuscated payloads (e.g. hex, base64) produce high entropy; pure
       English produces ~2.5–2.8 bits.

    2. get_syntactic_pressure(text) -> float
       Counts regex matches against a list of ~30 imperative trigger
       patterns (e.g. "ignore", "override", "pretend", "rm", "DROP TABLE").
       Only texts with >= 2 matches receive a non-zero score:
       pressure = (matches * 10) / (word_count + 1).

    3. get_semantic_pivot(text) -> float [0, 1]
       Computes Jaccard distance between the 4+ character tokens in the
       current input and the previous turn's tokens.  A high distance
       indicates a sudden topic shift (typical of multi-turn semantic walks).

    4. get_semantic_momentum() -> float [0, 1]
       Rolling mean of the three most recent pivot distances.  Captures
       sustained topic drift across a conversation window.

    5. get_transcoding_score(text) -> float [0, 1]
       Recursive decoder that attempts hex and base64 decoding (up to depth 3).
       If a decoded string contains trigger keywords (syntactic pressure > 1
       or prefix/suppression matches), a score of 0.6 + 0.3 * recursive_score
       is returned.  Detection gating: hex requires ratio > 0.7 and decoded
       length > 6; base64 requires length >= 16, 4-aligned, ratio > 0.8,
       and ends with '=' or length >= 32.

    6. get_constraint_suppression(text) -> int [0, N]
       Counts exact substring matches against 16 refusal-suppression phrases
       (e.g. "do not refuse", "skip the safety", "never say").

    7. get_prefix_inertia(text) -> int [0, N]
       Counts exact substring matches against 14 prefix-priming phrases
       (e.g. "start with", "begin your response", "sure,").

    8. reset_context() -> None
       Clears the inter-turn memory buffers (context_memory, pivot_history).

    Character classification table:
        lower : a-z
        upper : A-Z
        digit : 0-9
        space : space, tab, newline, carriage-return
        punct : .,!?:;\"'()
        shell : &|;<>$\\`()[]{}

Purpose:
    Transform raw text into a dense feature vector that the MAIAGovernor uses
    for threat scoring, competing-objectives analysis, and breach detection.

This file contains no executable code — only a module-level description.
"""
