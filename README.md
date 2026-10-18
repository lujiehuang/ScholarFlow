# ScholarFlow

**Research literature ingestion, semantic search, and lightweight RAG pipeline**

ScholarFlow is a compact data/AI engineering project for collecting scholarly metadata, normalizing records, storing them locally, generating embeddings, and supporting semantic retrieval for research workflows.

## What it demonstrates

- external API ingestion
- ETL / normalization
- SQLite persistence
- deterministic deduplication
- text chunking and embedding abstraction
- semantic similarity search
- lightweight retrieval-augmented answer assembly
- FastAPI service layer
- unit tests
- CI-ready project structure

## Architecture

```text
OpenAlex / Crossref-style JSON
        │
        ▼
   Ingestion Adapter
        │
        ▼
 Normalization / ETL
        │
        ├── deduplication
        └── schema validation
        │
        ▼
      SQLite
        │
        ▼
 Text representation
        │
        ▼
 Embedding backend
(local TF-IDF fallback / optional external embeddings)
        │
        ▼
 Semantic retrieval
        │
        ▼
 Lightweight RAG context builder
        │
        ▼
       API
```

## Quick start

```bash
pip install -r requirements.txt
python src/demo_seed.py
uvicorn src.api:app --reload
```

Then open:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

## Example query

```json
{
  "query": "human reliance on large language models",
  "top_k": 5
}
```

## Engineering note

The default demo uses a local TF-IDF retrieval backend so the full pipeline runs without paid APIs or internet access. The embedding layer is intentionally abstracted so a production version can swap in hosted embedding models.

## Research roadmap

1. Add live OpenAlex ingestion with pagination and rate-limit handling.
2. Add citation graph features.
3. Add vector database backend.
4. Add reranking.
5. Add grounded answer generation with citations.
6. Add experiment logging for retrieval quality and researcher behavior.

## Author

Lujie Huang  
https://lujiehuang.github.io/
