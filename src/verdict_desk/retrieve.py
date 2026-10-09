from __future__ import annotations

import math
import re
from collections import Counter

from verdict_desk.models import Chunk

TOKEN = re.compile(r"[a-z0-9]+")
STOP = {
    "a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "is", "are",
    "what", "how", "do", "does", "we", "i", "our", "be", "this", "that",
}


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP and len(t) > 1]


class Bm25Index:
    """Small BM25 index. Enough for a few dozen canonical docs; not a vector store."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.docs = [tokenize(f"{c.heading} {c.text}") for c in chunks]
        self.df: Counter[str] = Counter()
        for tokens in self.docs:
            self.df.update(set(tokens))
        self.n = len(self.docs)
        self.avgdl = sum(len(d) for d in self.docs) / max(self.n, 1)

    def search(self, query: str, k: int = 6) -> list[tuple[Chunk, float]]:
        q = tokenize(query)
        if not q:
            return []
        scored: list[tuple[Chunk, float]] = []
        for chunk, tokens in zip(self.chunks, self.docs):
            tf = Counter(tokens)
            dl = len(tokens) or 1
            score = 0.0
            for term in q:
                if term not in tf:
                    continue
                idf = math.log(1 + (self.n - self.df[term] + 0.5) / (self.df[term] + 0.5))
                denom = tf[term] + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                score += idf * (tf[term] * (self.k1 + 1)) / denom
            if score > 0:
                scored.append((chunk, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:k]
