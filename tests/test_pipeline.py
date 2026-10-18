import tempfile
import unittest
from pathlib import Path

from src.etl import normalize_record, deduplicate
from src.store import PaperStore
from src.retrieval import SemanticIndex

class ScholarFlowTests(unittest.TestCase):
    def test_normalize_and_deduplicate(self):
        a = normalize_record({"id":"1","title":"  Test   Paper ","authors":["A"]})
        b = normalize_record({"id":"2","title":"Test Paper","authors":["B"]})
        out = deduplicate([a,b])
        self.assertEqual(len(out),1)
        self.assertEqual(out[0].title,"Test Paper")

    def test_store_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"db.sqlite"
            store = PaperStore(path)
            p = normalize_record({"id":"1","title":"Human AI Reliance","abstract":"reflection and verification"})
            store.upsert_many([p])
            rows = store.all()
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0].paper_id,"1")

    def test_semantic_search(self):
        papers = [
            normalize_record({"id":"1","title":"Human AI Reliance","abstract":"users verify AI advice"}),
            normalize_record({"id":"2","title":"Database Systems","abstract":"query processing and indexes"})
        ]
        hits = SemanticIndex(papers).search("AI advice verification", top_k=1)
        self.assertEqual(hits[0].paper.paper_id,"1")

if __name__ == "__main__":
    unittest.main()
