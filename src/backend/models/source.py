"""Modelos Pydantic para la entidad Fuente RSS."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UpdateFrequency(str, Enum):
    hourly = "hourly"
    daily = "daily"
    weekly = "weekly"


class SourceBase(BaseModel):
    name: str
    url: str
    mediaOutlet: Optional[str] = None
    category: str
    iptcCode: Optional[str] = None
    language: str = "en"
    updateFrequency: UpdateFrequency = UpdateFrequency.hourly


class SourceCreate(SourceBase):
    pass


class SourceInDB(SourceBase):
    id: Optional[str] = None
    active: bool = True
    lastUpdated: Optional[datetime] = None
    nextUpdate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class SourceResponse(SourceBase):
    id: Optional[str] = None
    active: bool
    lastUpdated: Optional[datetime] = None
    createdAt: datetime
