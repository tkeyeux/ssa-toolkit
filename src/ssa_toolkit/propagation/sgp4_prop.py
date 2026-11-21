"""Thin, typed wrapper around the Vallado 'sgp4' library."""

from dataclasses import dataclass

import numpy as np 
from sgp4.api import Satrec, jday

@dataclass
class State:
    """Cartesian state in TEME frame. Position/velocity in km, km/s."""
    position: np.ndarray
    velocity: np.ndarray
    epoch_jd: float
    error: int

def parse_tle(line1: str, line2: str) -> Satrec:
    """Build an SGP4 propagator object from two TLE lines."""
    sat = Satrec.twoline2rv(line1.strip(), line2.strip())
    if sat.error != 0:
        raise ValueError(f"TLE parse error code {sat.error} for NORAD {sat.satnum}")
    return sat

def propagate(sat: Satrec, jd: float, fr: float) -> State:
    """Propagate to a Julian date (jd + fraction of day). Output in TEME, km."""

    e, r, v = sat.sgp4(jd, fr)
    if e != 0:
        raise RuntimeError(f"SGP4 propagation error {e} for NORAD {sat.satnum}")
    return State(position=np.asarray(r), velocity=np.asarray(v), epoch_jd=jd + fr, error=e)

def propagate_minutes(sat: Satrec, minutes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized propagation from TLE epoch: minutes from epoch -> (N,3) pos & vel arrays in km."""
    r, v = [], []
    for m in minutes:
        jd, fr = sat.jdsatepoch, sat.jdsatepochF + m /1440.0
        e, ri, vi = sat.sgp4(jd, fr)
        if e != 0:
            raise RuntimeError(f"SGP4 error {e} at t={m} min")
        r.append(ri)
        v.append(vi)
    return np.asarray(r), np.asarray(v)

def geodetic_altitude_km(r: nr.ndarray) -> float:
    """Quick altitude check: distance from geocenter minus Earth mean radius."""
    return float(np.linalg.norm(r)) - 6371.0088

__all__ = ["State", "parse_tle", "propagate", "propagate_minutes", "geodetic_altitude_km", "jday"]