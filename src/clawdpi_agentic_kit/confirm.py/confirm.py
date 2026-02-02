from __future__ import annotations

import os
import sys
from dataclasses import dataclass


class ConfirmationError(RuntimeError):
    pass


@dataclass
class ConfirmConfig:
    env_var: str = "CLAWDPI_CONFIRM"
    default: bool = False


def confirm(prompt: str, *, cfg: ConfirmConfig | None = None) -> bool:
    """Confirmation gate.

    Rules:
    - If env var exists: truthy => yes, falsy => no
    - If non-interactive (no TTY): return cfg.default
    - Else prompt user.
    """

    cfg = cfg or ConfirmConfig()

    if cfg.env_var in os.environ:
        v = os.environ.get(cfg.env_var, "").strip().lower()
        return v in {"1", "true", "yes", "y", "ok", "on"}

    if not sys.stdin.isatty():
        return cfg.default

    while True:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"", "n", "no"}:
            return False


def require_confirm(prompt: str, *, cfg: ConfirmConfig | None = None) -> None:
    if not confirm(prompt, cfg=cfg):
        raise ConfirmationError("Not confirmed")
