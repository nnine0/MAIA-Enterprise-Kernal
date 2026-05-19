import math
import re
import base64
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
        r"\bignore all\b",
        r"\bforget everything\b",
        r"\bwrite a story where\b",
        r"\bnow you are\b",
        r"\byou are now\b",
        r"\bpretend you are\b",
        r"\byou are\b",
        r"\bact as\b",
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

    SUPPRESSION_TERMS = [
        "ignore", "skip", "don't apologize", "no warnings",
        "without mention", "stop being", "do not refuse",
        "do not say you're sorry", "do not mention safety",
        "don't refuse", "don't apologize", "skip the safety",
        "without saying", "never say", "avoid ethical",
    ]

    PREFIX_PRIMING = [
        "start with", "begin your response",
        "sure,", "absolutely,", "certainly,", "of course,",
        "first word should be", "prefix with",
        "begin by saying", "start your answer",
        "i'd be happy", "okay,",
    ]

    def __init__(self, context_window: int = 5):
        self.context_memory: List[Set[str]] = []
        self.context_window = context_window
        self.pivot_history: List[float] = []

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
            self.pivot_history.append(0.0)
            return 0.0
        previous = self.context_memory[-1]
        intersection = current.intersection(previous)
        union = current.union(previous)
        distance = 1.0 - (len(intersection) / len(union)) if union else 0.0
        self.context_memory.append(current)
        self.pivot_history.append(distance)
        if len(self.context_memory) > self.context_window:
            self.context_memory.pop(0)
        if len(self.pivot_history) > self.context_window:
            self.pivot_history.pop(0)
        return distance

    def get_transcoding_score(self, text: str) -> float:
        score = 0.0
        stripped = re.sub(r'\s', '', text)
        n = len(stripped)
        if n < 8:
            return 0.0
        hex_ratio = sum(1 for c in stripped if c in '0123456789abcdefABCDEF') / n
        if hex_ratio > 0.7:
            try:
                decoded = bytes.fromhex(stripped).decode('utf-8', errors='ignore')
                if len(decoded) > 6 and self.get_syntactic_pressure(decoded) > 1.0:
                    score += 0.6
            except ValueError:
                pass
        if n >= 16 and n % 4 == 0:
            b64_chars = sum(1 for c in stripped
                            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                   'abcdefghijklmnopqrstuvwxyz'
                                   '0123456789+/=')
            if b64_chars / n > 0.8 and (stripped.endswith('=') or n >= 32):
                try:
                    decoded = base64.b64decode(stripped).decode('utf-8', errors='ignore')
                    if len(decoded) > 10 and self.get_syntactic_pressure(decoded) > 1.0:
                        score += 0.6
                except Exception:
                    pass
        return min(score, 1.0)

    def get_constraint_suppression(self, text: str) -> int:
        text_lower = text.lower()
        return sum(1 for term in self.SUPPRESSION_TERMS if term in text_lower)

    def get_prefix_inertia(self, text: str) -> int:
        text_lower = text.lower()
        return sum(1 for term in self.PREFIX_PRIMING if term in text_lower)

    def get_semantic_momentum(self) -> float:
        if len(self.pivot_history) < 2:
            return 0.0
        window = self.pivot_history[-3:]
        return sum(window) / len(window)

    def reset_context(self):
        self.context_memory.clear()
        self.pivot_history.clear()
