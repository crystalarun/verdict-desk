from __future__ import annotations

import argparse
import json
import os
import sys

from verdict_desk.engine import Desk


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ask Verdict Desk a question.")
    parser.add_argument("question", nargs="*", help="Question to ask")
    parser.add_argument("--corpus", default=os.environ.get("VERDICT_CORPUS"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    question = " ".join(args.question).strip()
    if not question:
        parser.error("Pass a question, e.g. verdict 'What is 30-day churn?'")
    desk = Desk(corpus_dir=args.corpus)
    verdict = desk.ask(question)
    if args.json:
        json.dump(verdict.to_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"{verdict.decision.upper()}: {verdict.reason}")
        if verdict.statement:
            print(verdict.statement)
        for cite in verdict.citations:
            print(f"- {cite.doc_id} ({cite.status}) [{cite.locator}]")
    return 0 if verdict.decision in {"answer", "conflict"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
