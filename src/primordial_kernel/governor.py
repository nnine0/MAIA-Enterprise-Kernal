import asyncio
import math
import logging
import time
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, asdict

from .abacus import Abacus
from .signal_encoder import AdvancedRegulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIA-Kernel")


@dataclass
class SafetyEvent:
    timestamp: float
    entropy: float
    syntactic_pressure: float
    semantic_pivot: float
    threat_score: float
    latency_applied: float
    aggregate_health: float
    is_breach: bool
    circuit_breaker_active: bool
    input_snippet: str


class MAIAGovernor:
    def __init__(
        self,
        entropy_threshold: float = 2.2,
        threat_threshold: float = 1.5,
        circuit_breaker_min: float = 0.2,
    ):
        self.abacus = Abacus()
        self.regulator = AdvancedRegulator()
        self.entropy_threshold = entropy_threshold
        self.threat_threshold = threat_threshold
        self.circuit_breaker_min = circuit_breaker_min
        self.hooks: List[Callable[[SafetyEvent], Any]] = []

    def add_hook(self, callback: Callable[[SafetyEvent], Any]):
        self.hooks.append(callback)

    async def process_signal(self, payload: str) -> Dict[str, Any]:
        entropy = self.regulator.get_character_entropy(payload)
        syntax = self.regulator.get_syntactic_pressure(payload)
        pivot = self.regulator.get_semantic_pivot(payload)
        threat = (entropy * 0.3) + (syntax * 0.5) + (pivot * 0.8)

        circuit_active = self.abacus.aggregate_health < self.circuit_breaker_min
        latency = 0.0
        is_breach = False

        if circuit_active:
            is_breach = True
        elif (entropy > self.entropy_threshold) or (threat > self.threat_threshold):
            is_breach = True
            latency = math.exp(threat) / 10
            self.abacus.drain(0.05 * threat)
            await asyncio.sleep(latency)
        else:
            self.abacus.recover(0.01)

        event = SafetyEvent(
            timestamp=time.time(),
            entropy=round(entropy, 4),
            syntactic_pressure=round(syntax, 4),
            semantic_pivot=round(pivot, 4),
            threat_score=round(threat, 4),
            latency_applied=round(latency, 4),
            aggregate_health=round(self.abacus.aggregate_health, 4),
            is_breach=is_breach,
            circuit_breaker_active=circuit_active,
            input_snippet=payload[:60] + "..." if len(payload) > 60 else payload,
        )

        self._emit_event(event)
        return asdict(event)

    def _emit_event(self, event: SafetyEvent):
        logger.info(json.dumps(asdict(event)))
        for hook in self.hooks:
            if asyncio.iscoroutinefunction(hook):
                asyncio.create_task(hook(event))
            else:
                hook(event)

    def reset_conversation(self):
        self.regulator.reset_context()
