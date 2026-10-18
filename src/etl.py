from __future__ import annotations
import re
from typing import Iterable
from src.schema import Paper

def _clean(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

def normalize_record(raw: dict) -> Paper:
    authors = raw.get("authors") or []
    if authors and isinstance(authors[0], dict):
        authors = [
            _clean(a.get("name") or a.get("display_name"))
            for a in authors
            if _clean(a.get("name") or a.get("display_name"))
        ]
    else:
        authors = [_clean(a) for a in authors if _clean(a)]

    paper_id = str(raw.get("paper_id") or raw.get("id") or raw.get("doi") or raw.get("title") or "").strip()
    if not paper_id:
        raise ValueError("record has no usable identifier")

    return Paper(
        paper_id=paper_id,
        title=_clean(raw.get("title")),
        abstract=_clean(raw.get("abstract")),
        year=raw.get("year"),
        venue=_clean(raw.get("venue")),
        doi=_clean(raw.get("doi")),
        authors=authors,
    )

def deduplicate(papers: Iterable[Paper]) -> list[Paper]:
    seen = set()
    out = []
    for p in papers:
        key = (p.doi.lower().strip() if p.doi else p.title.lower().strip())
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out
