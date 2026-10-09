from __future__ import annotations

import re
from pathlib import Path

from verdict_desk.models import Chunk, Document

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def _parse_front_matter(raw: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER.match(raw)
    if not match:
        return {}, raw.strip()
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, match.group(2).strip()


def _split_chunks(doc: Document) -> list[Chunk]:
    parts = re.split(r"(?m)^(#{2,3} .+)$", doc.body)
    chunks: list[Chunk] = []
    preamble = parts[0].strip()
    heading_chunks_exist = len(parts) > 1
    if preamble and not (heading_chunks_exist and len(preamble) < 220):
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}#intro",
                doc=doc,
                heading=doc.title,
                text=preamble,
                locator="intro",
            )
        )
    for i in range(1, len(parts), 2):
        heading = parts[i].lstrip("# ").strip()
        text = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if not text:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}#{slug}",
                doc=doc,
                heading=heading,
                text=text,
                locator=slug,
            )
        )
    return chunks


def load_corpus(root: str | Path) -> list[Chunk]:
    root = Path(root)
    documents: list[Document] = []
    for path in sorted(root.rglob("*.md")):
        meta, body = _parse_front_matter(path.read_text(encoding="utf-8"))
        documents.append(
            Document(
                doc_id=meta.get("id", path.stem),
                title=meta.get("title", path.stem.replace("_", " ").title()),
                doc_type=meta.get("type", "note"),
                status=meta.get("status", "canonical"),
                owner=meta.get("owner", "analytics"),
                metric_id=meta.get("metric_id") or None,
                path=str(path),
                body=body,
                sensitivity=meta.get("sensitivity", "internal"),
            )
        )
    chunks: list[Chunk] = []
    for doc in documents:
        chunks.extend(_split_chunks(doc))
    if not chunks:
        raise ValueError(f"No markdown documents found under {root}")
    return chunks
