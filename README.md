# ssa-toolkit

Open-source toolkit for orbital tracking, collision probability and space
debris anomaly detection.

Built on public data (CelesTrak TLEs, NOAA space weather, TraCSS test cases).

- `src/propagation` — SGP4/SDP4 wrapper, validated
- `data/download_celestrak.py` — public catalog ingestion

## Quickstart

    pip install -e ".[dev]"
    python data/download_celestrak.py
    pytest