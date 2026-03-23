"""Modelos Pydantic para la entidad Artículo (noticia indexada)."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class IptcTopic(BaseModel):
    code: str
    name: str
    confidence: float = 0.0
    manual: bool = False


class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    link: Optional[str] = None
    author: Optional[str] = None
    pubDate: datetime
    sourceId: str
    image: Optional[str] = None
    language: Optional[str] = None


class ArticleInDB(ArticleBase):
    id: Optional[str] = None
    hash: str
    iptcTopics: List[IptcTopic] = []
    alertMatches: List[str] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class ArticleResponse(ArticleBase):
    id: Optional[str] = None
    iptcTopics: List[IptcTopic] = []
    createdAt: datetime
