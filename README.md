# SpaceSituationalAwareness

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![PyTorch](https://img.shields.io/badge/pytorch-2.x-red.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status: Research](https://img.shields.io/badge/status-research-orange.svg)]()

**SSA** is a modular, open-source framework for Space Situational Awareness,
covering orbital propagation, conjunction assessment, and behavioral anomaly
detection of catalogued space objects.

Built entirely on **public data** (Celestrak TLEs, NOAA space weather, TraCSS
test cases), the project implements and benchmarks:

| Module | Scope |
|--------|-------|
| **Orbital propagation** | SGP4/SDP4 with ML-based residual correction (LSTM on SGP4 residual) |
| **Conjunction screening** | Cascaded filtering (altitude → orbital elements → XGBoost) + 2D collision probability (Gauss-Legendre / Monte-Carlo) |
| **Anomaly detection** | IMM-UKF (3 models), online decorrelation ($R_t$), Physics-Informed Orbital Transformer (PIOT) |
| **Space weather** | Kp / F10.7 ingestion, exponential drag correction, CNN flare forecasting |
| **Event detection** | Maneuvers, re-entry prediction, fragmentation |

Each module is accompanied by a **LaTeX paper**, reproducible benchmarks, and unit tests.

> **Status:** Research prototype. All results are measured on public or synthetic datasets.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Event Bus / Tracker                          │
└─────────────────────────────────────────────────────────────────────┘
         ▲               ▲                ▲                ▲
         │               │                │                │
┌────────┴─────┐  ┌──────┴──────┐  ┌──────┴──────┐  ┌─────┴──────┐
│  Propagation │  │ Conjunction │  │   Anomaly   │  │  Space Wx  │
│  SGP4 + LSTM │  │ N1→N4 + Pc  │  │ IMM-UKF     │  │ Kp, F10.7  │
│              │  │             │  │ PIOT, R_t   │  │ Drag corr. │
└──────┬───────┘  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘
       │                 │                │               │
       └─────────────────┴────────────────┴───────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   TLE Ingestion   │
                    │  (Celestrak API)  │
                    └───────────────────┘
```

---

## Installation

### Requirements

## Quick Start

### Run all benchmarks

## Project Structure

## Papers

## Benchmarks

## Data Sources

| Source | Content | Access |
|--------|---------|--------|
| [Celestrak](https://celestrak.org) | TLEs (30k+ objects), updated daily | Free, no auth |
| [NOAA SWPC](https://www.swpc.noaa.gov) | Kp, F10.7, solar flux | Free API |
| [TraCSS](https://github.com/ianmc11/tra-collision-test-set) | Conjunction test cases (NASA) | Public |
| [Space-Track](https://space-track.co) | Extended TLE history | Free account |

## Testing

## License

[MIT](LICENSE)

---

## Disclaimer

This project is a **research prototype** for educational and scientific purposes.
All data used is public or synthetic.
