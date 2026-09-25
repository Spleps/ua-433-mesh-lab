# Claude handoff context

This repository is a one-day analytical prototype related to Sviatoslav's scientific work:
an own-design 433 MHz UA_433 LoRa mesh pager for short small-unit messages.

The deliberately limited scope is:

- model a few nodes and links;
- select a fast profile for short links and a robust profile for longer links;
- estimate latency from LoRa-style spreading factor and bandwidth parameters;
- reject expired and replayed one-time packets;
- keep the implementation dependency-free and easy to explain in a student report.

Do not turn this prototype into a full military communications system without an explicit request.
It is not a security-certified implementation and must not be presented as one.

The main user-facing language is English in source files and README. The user communicates in
Russian; Ukrainian can be used for university-facing explanatory text.

