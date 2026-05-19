import numpy as np

class Abacus:
    """The Physical Substrate. Represents 1024 Logic Gates (Beads)."""
    def __init__(self, width=1024):
        self.beads = np.zeros(width, dtype=np.float16)
        self.health = 1.0

    def __repr__(self):
        mean_voltage = np.mean(self.beads)
        return f"<Abacus Voltage={mean_voltage:+.4f} Health={self.health:.2f}>"

    def update(self, signal):
        self.beads = np.tanh(self.beads + signal.astype(np.float16))
