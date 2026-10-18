## ScholarFlow — Literature ETL, Semantic Search & RAG Pipeline

**Python · FastAPI · SQLite · ETL · Semantic Retrieval · RAG**

Built an end-to-end scholarly data pipeline that normalizes literature records, removes duplicates, persists metadata in SQLite, constructs a local semantic index, and exposes retrieval plus RAG-context generation through an API. The architecture separates ingestion, storage, retrieval, and serving so hosted embedding or vector-database backends can be substituted later.
