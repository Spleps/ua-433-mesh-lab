# UA-433 Mesh Lab

Small, reproducible Python simulation of an adaptive LoRa-style mesh for short tactical messages.

The project is a one-day research prototype for the custom 433 MHz pager concept. It compares a
low-latency radio profile for nearby nodes with a robust profile for longer relay hops, while
demonstrating packet expiry and replay protection.

## What it demonstrates

- route discovery over a small multi-hop topology;
- adaptive radio profiles (`SF7/BW500` nearby and `SF10/BW125` for longer hops);
- deterministic airtime and latency estimates;
- one-time packet IDs, expiry windows, and duplicate rejection;
- JSON output suitable for a report or later plotting.

This is an analytical model, not a certified radio implementation. It does not replace testing
with SX126x hardware or regulatory review.

## Quick start

```powershell
py -m ua433_mesh --demo
py -m pytest
```

Example JSON output:

```json
{
  "route": ["alpha", "bravo", "charlie"],
  "radio_profiles": ["fast", "robust"],
  "estimated_latency_ms": 72.0,
  "delivered": true,
  "replay_accepted": false
}
```

## Repository layout

```text
ua433_mesh/
  __main__.py       CLI demo
  model.py          nodes, packets, radio profiles
  simulation.py     routing and delivery simulation
tests/
CLAUDE_CONTEXT.md  handoff context for future Claude sessions
```

## Research question

For a short message within a small squad, can a low-latency profile be used on nearby hops while
the mesh switches to a more robust profile for longer hops? The simulator makes the trade-off
explicit through estimated airtime and hop latency.

