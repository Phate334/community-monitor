from datetime import datetime

from pydantic import BaseModel


class ArxivArticle(BaseModel):
    id: str
    arxiv_id: str
    published: float  # timestamp
    title: str
    summary: str
    primary_category: str
    tags: list[str]
