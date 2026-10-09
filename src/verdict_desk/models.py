from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Decision = Literal["answer", "abstain", "block", "conflict"]


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    doc_type: str
    status: str
    owner: str
    metric_id: str | None
    path: str
    body: str
    sensitivity: str = "internal"


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc: Document
    heading: str
    text: str
    locator: str


@dataclass(frozen=True)
class Citation:
    doc_id: str
    title: str
    locator: str
    quote: str
    status: str


@dataclass
class Verdict:
    decision: Decision
    question: str
    statement: str | None
    reason: str
    citations: list[Citation] = field(default_factory=list)
    metric_ids: list[str] = field(default_factory=list)
    residual_risk: str = ""

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "question": self.question,
            "statement": self.statement,
            "reason": self.reason,
            "citations": [c.__dict__ for c in self.citations],
            "metric_ids": self.metric_ids,
            "residual_risk": self.residual_risk,
        }
