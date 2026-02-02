from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path


def default_state_path(app: str = "clawdpi-agentic-kit") -> Path:
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / app / "ratelimit.json"


@dataclass
class RateLimit:
    """Simple token bucket.

    rate_per_sec: tokens replenished per second
    burst: maximum tokens
    key: separate buckets per key
    """

    rate_per_sec: float
    burst: float
    key: str = "default"
    state_path: Path | None = None

    def _load(self) -> dict:
        path = self.state_path or default_state_path()
        try:
            raw = path.read_text(encoding="utf-8")
            return json.loads(raw)
        except Exception:
            return {}

    def _save(self, st: dict) -> None:
        path = self.state_path or default_state_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            return

    def acquire(self, tokens: float = 1.0, *, sleep: bool = True) -> bool:
        now = time.time()
        st = self._load()
        b = st.get(self.key) or {}
        last = float(b.get("t", now))
        avail = float(b.get("a", self.burst))

        # refill
        avail = min(self.burst, avail + (now - last) * self.rate_per_sec)

        if avail >= tokens:
            avail -= tokens
            st[self.key] = {"t": now, "a": avail}
            self._save(st)
            return True

        if not sleep:
            st[self.key] = {"t": now, "a": avail}
            self._save(st)
            return False

        # sleep until enough tokens
        need = tokens - avail
        delay = max(0.0, need / max(self.rate_per_sec, 1e-9))
        time.sleep(delay)
        return self.acquire(tokens=tokens, sleep=False)
