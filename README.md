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

## How the demo works

The built-in topology contains three nodes: `alpha` at 0 m, `bravo` at 250 m and `charlie` at
850 m. The first hop fits the fast profile, while the second hop is long enough to use the robust
profile. The simulator adds the estimated airtime and a small per-hop processing delay:

```text
alpha --250 m--> bravo --600 m--> charlie
fast              robust
```

For example, the `CONTACT` packet is accepted at `charlie` when it is still inside its validity
window. A second delivery attempt with the same packet ID is rejected, modelling a basic
anti-replay rule. If the relay is removed and no hop can cover the distance, the simulator raises
an explicit unreachable-route error.

## Scope and next steps

This repository is intentionally small and deterministic. It is useful for comparing design
choices and producing reproducible numbers in a report, but it does not model antenna gain,
interference, terrain, real LoRa headers, encryption, or a physical SX126x radio. A later version
could import measured link data and render latency/loss charts.
