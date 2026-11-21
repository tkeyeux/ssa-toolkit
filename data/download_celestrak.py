import sys
import time
from pathlib import Path

import requests

BASE = "https://celestrak.org/NORAD/elements/gp.php"
CACHE_DIR = Path(__file__).parent / "cache"

GROUPS = {
    "active": "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle",
    "starlink": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
    "oneweb": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=tle",
    "cosmos": "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-1408-debris&FORMAT=tle",
}

def download_group(name : str, url: str, retries: int = 3) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    out = CACHE_DIR / f"{name}.tle"
    for attempts in range(retries):
        r = requests.get(url, timeout=60, headers={"User-Agent": "ssa-toolkit/01 research"})
        if r.ok and len(r.text) > 100:
            out.write_text(r.text)
            n_lines : len(r.text.strip().striplines())
            print(f"{name}: {n_lines} lines -> {out}")
            return out
        print(f"{name}: attempt {attempt + 1} failed (HTTP {r.status_code}), retrying...")
        time.sleep(5)
    raise RuntimeError(f"Failed to download {name} after {retries} attempts")

def main() -> int: 
    groups = sys.argv[1:] if len(sys.argv) > 1 else list(GROUPS)
    for g in groups:
        download_group(g, GROUPS[g])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())