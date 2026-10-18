from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.store import PaperStore
from src.retrieval import SemanticIndex, build_rag_context

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "scholarflow.db"
app = FastAPI(title="ScholarFlow API", version="0.1.0")

class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)

@app.get("/health")
def health():
    return {"status":"ok", "db_ready":DB.exists()}

@app.post("/search")
def search(req: SearchRequest):
    store = PaperStore(DB)
    papers = store.all()
    index = SemanticIndex(papers)
    hits = index.search(req.query, req.top_k)
    return {
        "query": req.query,
        "results": [
            {
                "score": round(h.score,4),
                "paper_id": h.paper.paper_id,
                "title": h.paper.title,
                "year": h.paper.year,
                "venue": h.paper.venue,
                "authors": h.paper.authors
            } for h in hits
        ],
        "rag_context": build_rag_context(hits)
    }
