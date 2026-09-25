"""Domain objects for the small deterministic mesh model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    """A node positioned on a one-dimensional test route."""

    node_id: str
    position_m: float


@dataclass(frozen=True)
class RadioProfile:
    """Simplified LoRa profile used for comparative estimates."""

    name: str
    spreading_factor: int
    bandwidth_khz: int
    base_range_m: float
    airtime_ms: float


FAST_PROFILE = RadioProfile(
    name="fast",
    spreading_factor=7,
    bandwidth_khz=500,
    base_range_m=350,
    airtime_ms=24,
)

ROBUST_PROFILE = RadioProfile(
    name="robust",
    spreading_factor=10,
    bandwidth_khz=125,
    base_range_m=900,
    airtime_ms=48,
)


@dataclass(frozen=True)
class Packet:
    """A short-lived packet identified by a sender-scoped sequence number."""

    packet_id: str
    sender_id: str
    payload: str
    created_at_s: float
    valid_for_s: float = 30.0

    def is_valid_at(self, now_s: float) -> bool:
        return self.created_at_s <= now_s <= self.created_at_s + self.valid_for_s

