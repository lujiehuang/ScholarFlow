from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from src.schema import Paper

SCHEMA = '''
CREATE TABLE IF NOT EXISTS papers(
  paper_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  abstract TEXT,
  year INTEGER,
  venue TEXT,
  doi TEXT,
  authors_json TEXT
);
'''

class PaperStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as con:
            con.execute(SCHEMA)

    def upsert_many(self, papers: list[Paper]) -> int:
        with sqlite3.connect(self.path) as con:
            for p in papers:
                con.execute(
                    '''INSERT INTO papers VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(paper_id) DO UPDATE SET
                       title=excluded.title, abstract=excluded.abstract,
                       year=excluded.year, venue=excluded.venue,
                       doi=excluded.doi, authors_json=excluded.authors_json''',
                    (p.paper_id, p.title, p.abstract, p.year, p.venue, p.doi, json.dumps(p.authors))
                )
        return len(papers)

    def all(self) -> list[Paper]:
        with sqlite3.connect(self.path) as con:
            rows = con.execute("SELECT paper_id,title,abstract,year,venue,doi,authors_json FROM papers").fetchall()
        return [
            Paper(
                paper_id=r[0], title=r[1], abstract=r[2] or "", year=r[3],
                venue=r[4] or "", doi=r[5] or "", authors=json.loads(r[6] or "[]")
            ) for r in rows
        ]
