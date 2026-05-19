from typing import List


class Abacus:
    def __init__(self):
        self.health = 100.0
        self.history_vectors: List[float] = []

    @property
    def aggregate_health(self) -> float:
        return self.health / 100.0

    def record_turn(self, threat_score: float, is_breach: bool):
        self.history_vectors.append(threat_score)
        multiplier = 1.5 if is_breach else 1.0
        self.health -= (threat_score * 10 * multiplier)
        self.health = max(0.0, self.health)

    @property
    def momentum(self) -> float:
        if len(self.history_vectors) < 2:
            return 0.0
        recent = self.history_vectors[-3:]
        return sum(recent) / len(recent)
