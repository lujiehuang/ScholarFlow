from pydantic import BaseModel, Field
from typing import Optional

class Paper(BaseModel):
    paper_id: str
    title: str
    abstract: str = ""
    year: Optional[int] = None
    venue: str = ""
    doi: str = ""
    authors: list[str] = Field(default_factory=list)

    def searchable_text(self) -> str:
        return " ".join([
            self.title or "",
            self.abstract or "",
            self.venue or "",
            " ".join(self.authors or []),
        ]).strip()
