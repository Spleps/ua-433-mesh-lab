"""Command-line demo for the UA-433 Mesh Lab."""

import argparse
import json

from .model import Node, Packet
from .simulation import simulate_delivery


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a deterministic UA-433 mesh simulation")
    parser.add_argument("--demo", action="store_true", help="run the built-in three-node demo")
    args = parser.parse_args()
    if not args.demo:
        parser.error("pass --demo to run the built-in simulation")

    result = simulate_delivery(
        nodes=[Node("alpha", 0), Node("bravo", 250), Node("charlie", 850)],
        source_id="alpha",
        destination_id="charlie",
        packet=Packet("alpha-0001", "alpha", "CONTACT", created_at_s=100),
        now_s=105,
    )
    print(json.dumps({
        "route": result.route,
        "radio_profiles": result.profiles,
        "estimated_latency_ms": result.estimated_latency_ms,
        "delivered": result.delivered,
        "replay_accepted": result.replay_accepted,
    }, indent=2))


if __name__ == "__main__":
    main()

