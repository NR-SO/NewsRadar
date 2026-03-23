"""Modelos Pydantic para la entidad Alerta."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AlertKeyword(BaseModel):
    """Término de búsqueda con sinónimos (3-10 según especificación)."""
    term: str
    synonyms: List[str] = Field(default_factory=list)


class AlertBase(BaseModel):
    name: str
    keywords: List[AlertKeyword]
    iptcTopics: List[str] = []
    active: bool = True


class AlertCreate(AlertBase):
    pass


class AlertInDB(AlertBase):
    id: Optional[str] = None
    ownerId: str
    matchCount: int = 0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class AlertResponse(AlertBase):
    id: Optional[str] = None
    ownerId: str
    matchCount: int
    createdAt: datetime
    updatedAt: datetime
