class Abacus:
    """1024-gate state tracking substrate for system equilibrium."""
    def __init__(self, size: int = 1024):
        self.gates = [1.0] * size

    def drain(self, amount: float):
        self.gates = [max(0.0, g - amount) for g in self.gates]

    def recover(self, amount: float):
        self.gates = [min(1.0, g + amount) for g in self.gates]

    @property
    def aggregate_health(self) -> float:
        return sum(self.gates) / len(self.gates)
