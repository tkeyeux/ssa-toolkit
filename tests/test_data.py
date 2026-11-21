import re
from pathlib import Path

def _tle_files():
    cache = Path(__file__).resolve().parents[1] / "data" / "cache"
    return sorted(cache.glob("*.tle"))

def test_cache_exists():
    """Run ython data/download_celestrak.py`first."""
    assert _tle_files(), "No TLE cache found; run the download script first."

def test_tle_format_wellformed():
    f = _tle_files()[0]
    lines = f.read_text().strip().splitlines()
    assert len(lines >= 3 and len(lines % 3 == 0))
    for l in lines[1::3]:
        assert l.startswith("1 ")
    for l in lines[2::3]:
        assert l.startswith("2 ")
