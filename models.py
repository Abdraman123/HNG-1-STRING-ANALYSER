"""
Data models for both SQLAlchemy (database) and Pydantic (API validation).
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List
from datetime import datetime
from database import Base
from typing import Any


# ============= SQLAlchemy Models (Database Tables) =============

class StringAnalysisDB(Base):
    """
    SQLAlchemy model representing the strings table in the database.
    """
    __tablename__ = "strings"
    
    id = Column(String, primary_key=True)  # sha256 hash
    value = Column(String, unique=True, nullable=False, index=True)
    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_characters = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    sha256_hash = Column(String, nullable=False)
    character_frequency_map = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============= Pydantic Models (API Validation) =============

class StringProperties(BaseModel):
    """Properties computed from string analysis."""
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]


class StringAnalysisRequest(BaseModel):
    """Request model for POST /strings."""
    value: str = Field(..., min_length=1, description="String to analyze")
    
    @validator('value')
    def validate_value_type(cls, v):
        if not isinstance(v, str):
            raise ValueError('value must be a string')
        return v


class StringAnalysisResponse(BaseModel):
    """Response model for string analysis."""
    id: str
    value: str
    properties: StringProperties
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class StringListResponse(BaseModel):
    """Response model for GET /strings with filters."""
    data: List[StringAnalysisResponse]
    count: int
    filters_applied: Dict[str, Any]


class NaturalLanguageResponse(BaseModel):
    """Response model for natural language filtering."""
    data: List[StringAnalysisResponse]
    count: int
    interpreted_query: Dict[str, Any]