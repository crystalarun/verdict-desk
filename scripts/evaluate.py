from __future__ import annotations

import json
import sys
from pathlib import Path

from verdict_desk.engine import Desk

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "evals" / "golden.jsonl"


def main() -> int:
    desk = Desk(corpus_dir=ROOT / "corpus" / "dineflow")
    failed = 0
    for line in GOLDEN.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        verdict = desk.ask(case["question"])
        ok = verdict.decision == case["expect"]
        if ok and case.get("must_cite"):
            ok = any(c.doc_id == case["must_cite"] for c in verdict.citations)
        mark = "PASS" if ok else "FAIL"
        print(f"{mark} {case['id']:12} {verdict.decision}")
        failed += int(not ok)
    print(f"{failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
