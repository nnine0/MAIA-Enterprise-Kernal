import numpy as np

SHELL_META = set("$|&;`><~!#%(){}[]*?\\/@")
ALPHA_PUNCT = set(".,!?:;'\"-")

def classify_char(c):
    """Mutually exclusive character classification."""
    if 'a' <= c <= 'z':
        return 0  # lowercase
    if 'A' <= c <= 'Z':
        return 1  # uppercase
    if '0' <= c <= '9':
        return 2  # digit
    if c in ' \t\n\r':
        return 3  # whitespace
    if c in ALPHA_PUNCT:
        return 4  # punctuation
    if c in SHELL_META:
        return 5  # shell metacharacter
    return 6     # other

# Voltage mapping for each character class (evenly spaced across [-1, 1])
CLASS_VOLTAGE = np.array([-0.86, -0.57, -0.29, 0.0, 0.29, 0.57, 0.86], dtype=np.float16)


def text_to_signal(text, width=1024):
    """Encode text into a 1024-dimensional neural signal.

    Each character is mapped to one of 7 mutually exclusive classes:
    lowercase, uppercase, digit, whitespace, punctuation, shell-meta, other.
    Each class is assigned a distinct voltage level evenly spaced across [-1, 1].

    The entropy of this signal directly measures character-type diversity:
    pure natural language uses mostly lowercase+space+punct (3-4 classes),
    while dangerous payloads add shell-meta, digits, and mixed case (5-7 classes).
    """
    if not text:
        return np.full(width, CLASS_VOLTAGE[3], dtype=np.float16)

    voltages = [CLASS_VOLTAGE[classify_char(c)] for c in text[:width]]
    signal = np.array(voltages, dtype=np.float16)
    if len(signal) < width:
        signal = np.pad(signal, (0, width - len(signal)), mode="edge")
    return signal


def text_chaos(text):
    """Direct character-class entropy score without Abacus encoding.

    Computes Shannon entropy over the 7 character-class distribution.
    Normalized to [0, 1] where 0 = single class, 1 = uniform across all 7.
    This is the 'pure' chaos measure for any text signal.
    """
    if not text:
        return 0.0
    counts = np.zeros(7, dtype=float)
    for c in text:
        counts[classify_char(c)] += 1.0
    probs = counts / (counts.sum() + 1e-12)
    entropy = -np.sum(probs * np.log2(probs + 1e-12))
    return np.clip(entropy / np.log2(7), 0, 1)
