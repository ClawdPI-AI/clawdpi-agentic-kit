from __future__ import annotations

import argparse
import time


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="clawdpi-agentic-kit",
        description="Tiny agentic workflow primitives (v0.1).",
    )
    parser.add_argument("--version", action="store_true", help="Print version")
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep N seconds (demo)")
    args = parser.parse_args(argv)

    if args.version:
        try:
            from . import __version__
        except Exception:
            __version__ = "0.0.0"
        print(__version__)
        return 0

    if args.sleep > 0:
        time.sleep(args.sleep)

    print("clawdpi-agentic-kit is alive. Next: scopes/confirmations/rate-limit primitives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
