import math


class InertiaGuard:
    WEIGHTS = {"entropy": 0.2, "mismatched_gen": 0.5, "competing_obj": 0.4}

    @staticmethod
    def calculate_latency(threat_vector: dict) -> float:
        total = sum(threat_vector[k] * v for k, v in InertiaGuard.WEIGHTS.items())
        if total < 0.3:
            return 0.0
        latency = math.exp(total * 3) - 1
        return min(latency, 60.0)
