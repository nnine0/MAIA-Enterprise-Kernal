import math
import re
from typing import Set, List


class AdvancedRegulator:
    CHAR_CLASSES = {
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digit": "0123456789",
        "space": " \t\n\r",
        "punct": ".,!?:;\"'()",
        "shell": "&|;<>$\\`()[]{}",
    }

    IMPERATIVE_TRIGGERS = [
        # Single-word social engineering triggers
        r"\bignore\b",
        r"\bforget\b",
        r"\bsystem\b",
        r"\boverride\b",
        r"\bdeveloper\b",
        r"\bmode\b",
        r"\bunlocked\b",
        r"\bimagine\b",
        r"\bstrictly\b",
        r"\bpretend\b",
        r"\bnevermind\b",
        r"\bdisregard\b",
        # Multi-word composite triggers (stack with single-word for stronger signal)
        r"\bignore all\b",
        r"\bforget everything\b",
        r"\bwrite a story where\b",
        r"\bnow you are\b",
        r"\byou are now\b",
        r"\bpretend you are\b",
        r"\byou are\b",
        r"\bact as\b",
        # Shell / code injection commands
        r"\brm\b",
        r"\bchmod\b",
        r"\bchown\b",
        r"\bcurl\b",
        r"\bwget\b",
        r"\bbash\b",
        r"\bexec\b",
        r"\beval\b",
        r"\bsudo\b",
        r"\bdd\b",
        r"\bmkfs\b",
        r"\bfdisk\b",
        r"\bdrop\s+table\b",
        r"\bunion\s+select\b",
        r"\bpasswd\b",
        r"\bshadow\b",
    ]

    def __init__(self, context_window: int = 5):
        self.context_memory: List[Set[str]] = []
        self.context_window = context_window

    def get_character_entropy(self, text: str) -> float:
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

    def get_syntactic_pressure(self, text: str) -> float:
        text_lower = text.lower()
        matches = 0
        for pattern in self.IMPERATIVE_TRIGGERS:
            if re.search(pattern, text_lower):
                matches += 1
        if matches < 2:
            return 0.0
        return (matches * 10) / (len(text.split()) + 1)

    def get_semantic_pivot(self, text: str) -> float:
        current = set(re.findall(r'\w{4,}', text.lower()))
        if not self.context_memory:
            self.context_memory.append(current)
            return 0.0

        previous = self.context_memory[-1]
        intersection = current.intersection(previous)
        union = current.union(previous)
        distance = 1.0 - (len(intersection) / len(union)) if union else 0.0

        self.context_memory.append(current)
        if len(self.context_memory) > self.context_window:
            self.context_memory.pop(0)

        return distance

    def reset_context(self):
        self.context_memory.clear()
