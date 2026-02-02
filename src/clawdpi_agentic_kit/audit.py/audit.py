from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_audit_path(app: str = "clawdpi-agentic-kit") -> Path:
    base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / app / "audit.jsonl"


@dataclass
class AuditEvent:
    ts: str
    action: str
    ok: bool
    meta: dict[str, Any]


class AuditLogger:
    """Append-only JSONL audit log.

    Safe default: never throws on write errors.
    """

    def __init__(self, path: Path | None = None):
        self.path = path or default_audit_path()

    def log(self, action: str, ok: bool = True, **meta: Any) -> None:
        evt = AuditEvent(ts=_utc_now_iso(), action=action, ok=ok, meta=meta)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(evt), ensure_ascii=False) + "\n")
        except Exception:
            # audit should never crash the agent
            return
