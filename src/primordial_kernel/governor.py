import asyncio
import math
import logging
import time
import json
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, asdict

from .abacus import Abacus
from .signal_encoder import AdvancedRegulator
from .inertia_guard import InertiaGuard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIA-Kernel")


@dataclass
class SafetyEvent:
    timestamp: float
    entropy: float
    syntactic_pressure: float
    semantic_pivot: float
    semantic_momentum: float
    transcoding_score: float
    constraint_suppression: int
    prefix_inertia: int
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
        threat_threshold: float = 1.3,
        circuit_breaker_min: float = 0.2,
    ):
        self.abacus = Abacus()
        self.regulator = AdvancedRegulator()
        self.inertia_guard = InertiaGuard()
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
        momentum = self.regulator.get_semantic_momentum()
        transcoding = self.regulator.get_transcoding_score(payload)
        suppression = self.regulator.get_constraint_suppression(payload)
        prefix = self.regulator.get_prefix_inertia(payload)

        threat = (entropy * 0.2) + (syntax * 0.3) + (pivot * 0.3) + (momentum * 0.2)

        competing_obj = min(suppression * 0.25 + prefix * 0.2, 1.0)
        ig_vector = {
            "entropy": entropy,
            "mismatched_gen": transcoding,
            "competing_obj": competing_obj,
        }

        circuit_active = self.abacus.aggregate_health < self.circuit_breaker_min
        is_breach = circuit_active
        is_breach = is_breach or (entropy > self.entropy_threshold)
        is_breach = is_breach or (threat > self.threat_threshold)
        is_breach = is_breach or (transcoding > 0)
        is_breach = is_breach or (competing_obj > 0.3)

        latency = 0.0
        if is_breach and not circuit_active:
            latency = self.inertia_guard.calculate_latency(ig_vector)
            if latency > 0:
                await asyncio.sleep(latency)

        self.abacus.record_turn(threat, is_breach)

        event = SafetyEvent(
            timestamp=time.time(),
            entropy=round(entropy, 4),
            syntactic_pressure=round(syntax, 4),
            semantic_pivot=round(pivot, 4),
            semantic_momentum=round(momentum, 4),
            transcoding_score=round(transcoding, 4),
            constraint_suppression=suppression,
            prefix_inertia=prefix,
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
