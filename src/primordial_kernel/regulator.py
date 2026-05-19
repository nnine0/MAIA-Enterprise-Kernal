import numpy as np

class EntropyRegulator:
    """The Mathematical Guardian. Measures Shannon Entropy."""
    @staticmethod
    def calculate_chaos(signal):
        counts, _ = np.histogram(signal, bins=10, range=(-1, 1), density=True)
        probs = counts / (np.sum(counts) + 1e-9)
        entropy = -np.sum(probs * np.log2(probs + 1e-9))
        return np.clip(entropy / 3.32, 0, 1)
