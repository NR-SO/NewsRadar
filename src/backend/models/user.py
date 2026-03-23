"""Modelos Pydantic para la entidad Usuario."""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    gestor_newsradar = "gestor_newsradar"
    lector = "lector"


class UserPreferences(BaseModel):
    iptcSubscriptions: List[str] = []
    sourceSubscriptions: List[str] = []
    alertsEnabled: bool = True
    emailNotifications: bool = True
    language: str = "es"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole = UserRole.lector
    preferences: UserPreferences = Field(default_factory=UserPreferences)


class UserInDB(BaseModel):
    id: Optional[str] = None
    email: str
    name: str
    role: UserRole
    hashed_password: str
    active: bool = True
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastLogin: Optional[datetime] = None


class UserResponse(BaseModel):
    id: Optional[str] = None
    email: str
    name: str
    role: UserRole
    active: bool
    preferences: UserPreferences
    createdAt: datetime
