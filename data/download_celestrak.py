"""Download the current public TLE catalog from CelesTrak (free, no account)."""
import sys
import time
from pathlib import Path

import requests

CACHE_DIR = Path(__file__).parent / "cache"

GROUPS = {
    "active": "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle",
    "starlink": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
    "oneweb": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=tle",
    "cosmos-1408-debris": "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-1408-debris&FORMAT=tle",
}


def download_group(name: str, url: str, retries: int = 5) -> Path | None:
    CACHE_DIR.mkdir(exist_ok=True)
    out = CACHE_DIR / f"{name}.tle"
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=120,
                             headers={"User-Agent": "ssa-toolkit/0.1 research"})
        except requests.RequestException as exc:
            print(f"{name}: request failed ({exc}), attempt {attempt}/{retries}")
            time.sleep(30)
            continue
        if r.ok and len(r.text) > 100:
            out.write_text(r.text)
            n_lines = len(r.text.strip().splitlines())
            print(f"{name}: {n_lines} lines -> {out}")
            return out
        if r.status_code in (403, 429):
            # Celestrak rate limiting: back off strongly
            wait = 60 * attempt
            print(f"{name}: HTTP {r.status_code} (rate limit), waiting {wait}s...")
            time.sleep(wait)
        else:
            print(f"{name}: attempt {attempt}/{retries} failed (HTTP {r.status_code})")
            time.sleep(30)
    print(f"WARNING: {name} not downloaded right now; retry later.")
    return None


def main() -> int:
    groups = sys.argv[1:] if len(sys.argv) > 1 else list(GROUPS)
    failures = []
    for g in groups:
        if download_group(g, GROUPS[g]) is None:
            failures.append(g)
        time.sleep(20)  # be polite to the free service
    if failures:
        print(f"Failed groups (retry later): {', '.join(failures)}")
    return 0  # don't crash: partial cache is still useful


if __name__ == "__main__":
    raise SystemExit(main())