import time
import threading
import numpy as np
from .regulator import EntropyRegulator
from .signal_encoder import text_to_signal, text_chaos

class SiliconGovernor:
    """The Universal Tuner. Injects Latency to prevent Logic Collapse."""
    def __init__(self, abacus):
        self.abacus = abacus
        self.regulator = EntropyRegulator()
        self.resistance = 0.0
        self._lock = threading.Lock()

    def constrain(self, signal):
        if isinstance(signal, str):
            text = signal
            signal = text_to_signal(text)
            chaos_score = text_chaos(text)
        else:
            chaos_score = self.regulator.calculate_chaos(signal)

        self.abacus.update(signal)

        with self._lock:
            if chaos_score > 0.7:
                self.resistance = chaos_score * 0.1
                self.abacus.health -= 0.05
            else:
                self.resistance = max(0, self.resistance * 0.9)
                self.abacus.health = min(1.0, self.abacus.health + 0.01)

        if self.resistance > 0:
            time.sleep(self.resistance)

        return chaos_score

    def wrap_action(self, func):
        def wrapper(*args, **kwargs):
            signal = np.array(args[1:]) if len(args) > 1 else np.random.rand(10)
            self.constrain(signal)
            return func(*args, **kwargs)
        return wrapper
