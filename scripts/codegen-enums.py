"""X8 → Python + TypeScript ENUM codegen.

Round 25 scaffold: stub that reports its plan and exits 0. Round 26 replaces
this with a real markdown-table parser that emits:

  - packages/enums/python/src/epcc_enums/_generated.py
  - packages/enums/typescript/src/_generated.ts

Source of truth: SystemAdmin/Cross-link files/X8_GlossaryENUMs_v0_5.md
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
X8_DIR = REPO_ROOT / "SystemAdmin" / "Cross-link files"
PY_OUT = REPO_ROOT / "packages" / "enums" / "python" / "src" / "epcc_enums" / "_generated.py"
TS_OUT = REPO_ROOT / "packages" / "enums" / "typescript" / "src" / "_generated.ts"


def find_latest_x8() -> Path | None:
    candidates = sorted(X8_DIR.glob("X8_GlossaryENUMs_v*.md"))
    return candidates[-1] if candidates else None


def main() -> int:
    x8 = find_latest_x8()
    if x8 is None:
        print(f"ERROR: no X8 glossary found under {X8_DIR}", file=sys.stderr)
        return 1
    print(f"X8 source : {x8.relative_to(REPO_ROOT)}")
    print(f"Python out: {PY_OUT.relative_to(REPO_ROOT)}")
    print(f"TS out    : {TS_OUT.relative_to(REPO_ROOT)}")
    print()
    print("Round 25 scaffold — codegen not yet implemented. Round 26 replaces this stub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
