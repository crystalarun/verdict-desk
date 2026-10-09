from __future__ import annotations

import re
from pathlib import Path

from verdict_desk.catalog import load_corpus
from verdict_desk.models import Citation, Verdict
from verdict_desk.policy import inspect_question, mask_pii
from verdict_desk.retrieve import Bm25Index

DEFAULT_CORPUS = Path(__file__).resolve().parents[2] / "corpus" / "dineflow"
LEGACY_HINT = re.compile(
    r"legacy|superseded|old definition|login inactivity|versus|\bvs\b|previous definition",
    re.I,
)


def _quote(text: str, limit: int = 280) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


class Desk:
    def __init__(self, corpus_dir: str | Path | None = None, min_score: float = 1.2) -> None:
        self.corpus_dir = Path(corpus_dir) if corpus_dir else DEFAULT_CORPUS
        self.chunks = load_corpus(self.corpus_dir)
        self.index = Bm25Index(self.chunks)
        self.min_score = min_score

    def ask(self, question: str) -> Verdict:
        question = mask_pii(question.strip())
        blocked = inspect_question(question)
        if blocked:
            return Verdict(
                decision="block",
                question=question,
                statement=None,
                reason=blocked,
                residual_risk="Request never reached the corpus.",
            )

        hits = self.index.search(question, k=6)
        usable = [(chunk, score) for chunk, score in hits if score >= self.min_score]
        if not usable:
            return Verdict(
                decision="abstain",
                question=question,
                statement=None,
                reason="no_supporting_evidence",
                residual_risk="Do not invent a metric definition or a runbook step.",
            )

        metric_ids = sorted(
            {chunk.doc.metric_id for chunk, _ in usable if chunk.doc.metric_id}
        )
        statuses_by_metric: dict[str, set[str]] = {}
        for chunk, _ in usable:
            if not chunk.doc.metric_id:
                continue
            statuses_by_metric.setdefault(chunk.doc.metric_id, set()).add(chunk.doc.status)
        citations = [
            Citation(
                doc_id=chunk.doc.doc_id,
                title=chunk.doc.title,
                locator=chunk.locator,
                quote=_quote(chunk.text),
                status=chunk.doc.status,
            )
            for chunk, _ in usable[:3]
        ]

        conflicting = [
            mid
            for mid, statuses in statuses_by_metric.items()
            if "canonical" in statuses and "superseded" in statuses
        ]
        if conflicting and LEGACY_HINT.search(question):
            return Verdict(
                decision="conflict",
                question=question,
                statement=None,
                reason="canonical_and_superseded_definitions_both_retrieved",
                citations=citations,
                metric_ids=conflicting,
                residual_risk="Do not pick a definition until analytics confirms the canonical version.",
            )

        usable = [
            (chunk, score)
            for chunk, score in usable
            if chunk.doc.status != "superseded"
        ] or usable
        citations = [
            Citation(
                doc_id=chunk.doc.doc_id,
                title=chunk.doc.title,
                locator=chunk.locator,
                quote=_quote(chunk.text),
                status=chunk.doc.status,
            )
            for chunk, _ in usable[:3]
        ]

        ranked = sorted(
            usable,
            key=lambda item: (
                0 if item[0].doc.status == "canonical" else 1,
                -item[1],
            ),
        )
        top, _ = ranked[0]
        statement = _quote(top.text, limit=420)
        return Verdict(
            decision="answer",
            question=question,
            statement=statement,
            reason="supported_by_canonical_corpus",
            citations=citations[:2],
            metric_ids=metric_ids,
            residual_risk="Quote is extractive. It is not a live warehouse number.",
        )
