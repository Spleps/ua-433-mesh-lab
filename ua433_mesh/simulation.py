"""Routing and packet-delivery simulation."""

from dataclasses import dataclass
from math import ceil

from .model import FAST_PROFILE, ROBUST_PROFILE, Node, Packet, RadioProfile


@dataclass(frozen=True)
class SimulationResult:
    route: tuple[str, ...]
    profiles: tuple[str, ...]
    estimated_latency_ms: float
    delivered: bool
    replay_accepted: bool


def choose_profile(distance_m: float) -> RadioProfile:
    """Use the low-latency profile when a direct hop is comfortably short."""
    return FAST_PROFILE if distance_m <= FAST_PROFILE.base_range_m else ROBUST_PROFILE


def find_route(nodes: list[Node], source_id: str, destination_id: str) -> list[Node]:
    """Find a route through nodes ordered by position.

    The one-dimensional topology keeps the one-day prototype understandable: nodes must be
    ordered from source to destination, and every adjacent hop must fit the robust profile.
    """
    by_position = sorted(nodes, key=lambda node: node.position_m)
    source_index = next(i for i, node in enumerate(by_position) if node.node_id == source_id)
    destination_index = next(
        i for i, node in enumerate(by_position) if node.node_id == destination_id
    )
    if source_index > destination_index:
        by_position = list(reversed(by_position))
        source_index = next(i for i, node in enumerate(by_position) if node.node_id == source_id)
        destination_index = next(
            i for i, node in enumerate(by_position) if node.node_id == destination_id
        )
    route = by_position[source_index : destination_index + 1]
    if len(route) < 2 or any(
        route[i + 1].position_m - route[i].position_m > ROBUST_PROFILE.base_range_m
        for i in range(len(route) - 1)
    ):
        raise ValueError("destination is unreachable with the available relay nodes")
    return route


def simulate_delivery(
    nodes: list[Node],
    source_id: str,
    destination_id: str,
    packet: Packet,
    now_s: float,
) -> SimulationResult:
    """Deliver one packet and then attempt to replay it at the destination."""
    route = find_route(nodes, source_id, destination_id)
    profiles = tuple(
        choose_profile(route[i + 1].position_m - route[i].position_m).name
        for i in range(len(route) - 1)
    )
    latency = sum(
        choose_profile(route[i + 1].position_m - route[i].position_m).airtime_ms
        + 12
        for i in range(len(route) - 1)
    )
    delivered = packet.is_valid_at(now_s)
    seen_packets: set[str] = {packet.packet_id} if delivered else set()
    replay_accepted = packet.packet_id not in seen_packets and packet.is_valid_at(now_s)
    return SimulationResult(
        route=tuple(node.node_id for node in route),
        profiles=profiles,
        estimated_latency_ms=ceil(latency * 10) / 10,
        delivered=delivered,
        replay_accepted=replay_accepted,
    )

