from pathlib import Path
from src.etl import normalize_record, deduplicate
from src.store import PaperStore

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "scholarflow.db"

RAW = [
    {
        "id":"p1",
        "title":"Calibrating Reliance on AI Advice",
        "abstract":"We study when users accept, reject, and verify AI-generated advice in decision tasks.",
        "year":2024,
        "venue":"CHI",
        "authors":["A. Researcher","B. Author"]
    },
    {
        "id":"p2",
        "title":"Reflection Prompts in Human-AI Decision Making",
        "abstract":"This work examines reflective interventions designed to reduce passive acceptance of automated suggestions.",
        "year":2025,
        "venue":"CSCW",
        "authors":["C. Scholar"]
    },
    {
        "id":"p3",
        "title":"Retrieval-Augmented Generation for Scientific Literature",
        "abstract":"A retrieval pipeline indexes scientific documents and constructs evidence-grounded contexts for language models.",
        "year":2025,
        "venue":"ACL",
        "authors":["D. Scientist","E. Engineer"]
    },
    {
        "id":"p4",
        "title":"Human-Centered Evaluation of Large Language Models",
        "abstract":"We present behavioral and subjective metrics for evaluating interactive large language model systems.",
        "year":2024,
        "venue":"IUI",
        "authors":["F. HCI"]
    }
]

def main():
    papers = deduplicate([normalize_record(x) for x in RAW])
    store = PaperStore(DB)
    n = store.upsert_many(papers)
    print(f"seeded {n} papers -> {DB}")

if __name__ == "__main__":
    main()
