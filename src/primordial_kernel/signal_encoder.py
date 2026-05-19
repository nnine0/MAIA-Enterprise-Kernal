import math

class SignalRegulator:
    """Calculates Shannon Entropy based on character classes."""
    CHAR_CLASSES = {
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digit": "0123456789",
        "space": " \t\n\r",
        "punct": ".,!?:;\"'()",
        "shell": "&|;<>$\\`()[]{}",
    }

    def get_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        counts = {k: 0 for k in self.CHAR_CLASSES}
        counts["other"] = 0

        for char in text:
            found = False
            for category, charset in self.CHAR_CLASSES.items():
                if char in charset:
                    counts[category] += 1
                    found = True
                    break
            if not found:
                counts["other"] += 1

        probs = [count / len(text) for count in counts.values() if count > 0]
        return -sum(p * math.log2(p) for p in probs)
