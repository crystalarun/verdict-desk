from __future__ import annotations

import os
from functools import lru_cache

from verdict_desk.engine import Desk

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install API extras: pip install -e '.[api]'") from exc


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class AskResponse(BaseModel):
    decision: str
    question: str
    statement: str | None
    reason: str
    citations: list[dict]
    metric_ids: list[str]
    residual_risk: str


@lru_cache(maxsize=1)
def get_desk() -> Desk:
    return Desk(corpus_dir=os.environ.get("VERDICT_CORPUS"))


app = FastAPI(title="Verdict Desk", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/verdict", response_model=AskResponse)
def ask(req: AskRequest) -> dict:
    return get_desk().ask(req.question).to_dict()
