import asyncio
import math
import logging
import time
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, asdict

from .abacus import Abacus
from .signal_encoder import SignalRegulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAIA-Kernal")


@dataclass
class SafetyEvent:
    timestamp: float
    entropy: float
    latency_applied: float
    system_health: float
    is_breach: bool
    input_snippet: str


class MAIAGovernor:
    def __init__(self, entropy_threshold: float = 2.2):
        self.abacus = Abacus()
        self.regulator = SignalRegulator()
        self.threshold = entropy_threshold
        self.hooks: List[Callable[[SafetyEvent], Any]] = []

    def add_hook(self, callback: Callable[[SafetyEvent], Any]):
        self.hooks.append(callback)

    async def process_signal(self, payload: str) -> Dict[str, Any]:
        entropy = self.regulator.get_entropy(payload)
        latency = 0.0
        is_breach = False

        if entropy > self.threshold:
            latency = math.pow(2, (entropy - self.threshold) * 5) / 10
            self.abacus.drain(0.1 * (entropy / self.threshold))
            is_breach = True

            await asyncio.sleep(latency)
        else:
            self.abacus.recover(0.05)

        event = SafetyEvent(
            timestamp=time.time(),
            entropy=round(entropy, 4),
            latency_applied=round(latency, 4),
            system_health=round(self.abacus.aggregate_health, 4),
            is_breach=is_breach,
            input_snippet=payload[:50] + "..." if len(payload) > 50 else payload,
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
