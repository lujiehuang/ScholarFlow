from __future__ import annotations
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.schema import Paper

@dataclass(frozen=True)
class SearchHit:
    score: float
    paper: Paper

class SemanticIndex:
    def __init__(self, papers: list[Paper]):
        self.papers = papers
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=5000)
        corpus = [p.searchable_text() for p in papers]
        self.matrix = self.vectorizer.fit_transform(corpus) if corpus else None

    def search(self, query: str, top_k: int = 5) -> list[SearchHit]:
        if not self.papers or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix)[0]
        order = sims.argsort()[::-1][:top_k]
        return [SearchHit(float(sims[i]), self.papers[i]) for i in order if sims[i] > 0]

def build_rag_context(hits: list[SearchHit]) -> str:
    chunks = []
    for i, h in enumerate(hits, 1):
        p = h.paper
        chunks.append(
            f"[{i}] {p.title} ({p.year or 'n.d.'})\n"
            f"Venue: {p.venue or 'Unknown'}\n"
            f"Abstract: {p.abstract[:700]}"
        )
    return "\n\n".join(chunks)
