"""Non-regression tests for the SGP4 wrapper.

The reference TLE is the sample ISS TLE distributed with the 'sgp4' library itsel;
oracle values are recomputed with sgp4.api directly, so what we test here is the wrapper's correctness, not the library's."""

import numpy as np
import pytest

from sgp4.api import Satrec, jday

from ssa_toolkit.propagation import (geodetic_altitude_km, parse_tle, propagate, propagate_minutes)

LINE1 = "1 25544U 98067A   24050.54791425  .00016756  00000+0  30779-3 0  9993"
LINE2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.4951271944soo".replace("soo", "00")

@pytest.fixture
def iss() -> Satrec:
    return parse_tle(LINE1, LINE2)

def test_parse_ok(iss):
    assert iss.satnum == 25544
    assert iss.error == 0

def test_propagate_matches_library(iss):
    jd, fr = jday(2024, 2, 19, 12, 0, 0.0)
    state = propagate(iss, jd, fr)
    _, r_ref, v_ref = Satrec.twoline2rv(LINE1, LINE2).sgp4(jd, fr)
    assert state.error == 0
    assert np.allclose(state.position, r_ref, atol=1e-9)
    assert np.allclose(state.velocity, v_ref, atol=1e-12)

def test_energy_conservation(iss):
    """Vis-visa: specific energy must be constant along a short arc."""
    minutes = np.linspace(0, 45, 20)
    r, v = propagate_minutes(iss, minutes)
    energy = np.linalg.norm(v, axis=1) ** 2 / 2 - 398600.4418 / np.linalg.norm(r, axis=1)

    assert np.ptp(energy) < 1e-6