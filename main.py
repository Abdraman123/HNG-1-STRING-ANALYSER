"""
Main FastAPI application with all endpoints.
"""

from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from database import engine, get_db, Base
from models import (
    StringAnalysisRequest,
    StringAnalysisResponse,
    StringListResponse,
    NaturalLanguageResponse,
    StringProperties
)
from services import (
    analyze_string,
    create_string_analysis,
    get_string_by_value,
    delete_string_by_value,
    get_all_strings_with_filters,
    parse_natural_language_query
)
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RESTful API for analyzing and storing string properties"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= Endpoints =============

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "endpoints": {
            "POST /strings": "Analyze and store a new string",
            "GET /strings/{string_value}": "Retrieve a specific string",
            "GET /strings": "Get all strings with optional filters",
            "GET /strings/filter-by-natural-language": "Filter using natural language",
            "DELETE /strings/{string_value}": "Delete a string",
            "/docs": "Interactive API documentation"
        }
    }


@app.post("/strings", response_model=StringAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_string(
    request: StringAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze and store a new string.
    
    Returns 409 if string already exists.
    """
    # Check if string already exists
    existing = get_string_by_value(db, request.value)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="String already exists in the system"
        )
    
    # Analyze the string
    analysis_data = analyze_string(request.value)
    
    # Store in database
    db_string = create_string_analysis(db, analysis_data)
    
    # Format response
    return StringAnalysisResponse(
        id=db_string.id,
        value=db_string.value,
        properties=StringProperties(
            length=db_string.length,
            is_palindrome=db_string.is_palindrome,
            unique_characters=db_string.unique_characters,
            word_count=db_string.word_count,
            sha256_hash=db_string.sha256_hash,
            character_frequency_map=db_string.character_frequency_map
        ),
        created_at=db_string.created_at
    )


@app.get("/strings/{string_value}", response_model=StringAnalysisResponse)
async def get_string(string_value: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific string by its value.
    
    Returns 404 if not found.
    """
    db_string = get_string_by_value(db, string_value)
    
    if not db_string:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    return StringAnalysisResponse(
        id=db_string.id,
        value=db_string.value,
        properties=StringProperties(
            length=db_string.length,
            is_palindrome=db_string.is_palindrome,
            unique_characters=db_string.unique_characters,
            word_count=db_string.word_count,
            sha256_hash=db_string.sha256_hash,
            character_frequency_map=db_string.character_frequency_map
        ),
        created_at=db_string.created_at
    )


@app.get("/strings", response_model=StringListResponse)
async def get_all_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1),
    db: Session = Depends(get_db)
):
    """
    Get all strings with optional filtering.
    """
    # Get filtered strings
    strings = get_all_strings_with_filters(
        db=db,
        is_palindrome=is_palindrome,
        min_length=min_length,
        max_length=max_length,
        word_count=word_count,
        contains_character=contains_character
    )
    
    # Build filters_applied dict
    filters_applied = {}
    if is_palindrome is not None:
        filters_applied['is_palindrome'] = is_palindrome
    if min_length is not None:
        filters_applied['min_length'] = min_length
    if max_length is not None:
        filters_applied['max_length'] = max_length
    if word_count is not None:
        filters_applied['word_count'] = word_count
    if contains_character is not None:
        filters_applied['contains_character'] = contains_character
    
    # Format response
    data = [
        StringAnalysisResponse(
            id=s.id,
            value=s.value,
            properties=StringProperties(
                length=s.length,
                is_palindrome=s.is_palindrome,
                unique_characters=s.unique_characters,
                word_count=s.word_count,
                sha256_hash=s.sha256_hash,
                character_frequency_map=s.character_frequency_map
            ),
            created_at=s.created_at
        )
        for s in strings
    ]
    
    return StringListResponse(
        data=data,
        count=len(data),
        filters_applied=filters_applied
    )


@app.get("/strings/filter-by-natural-language", response_model=NaturalLanguageResponse)
async def filter_by_natural_language(
    query: str = Query(..., description="Natural language query"),
    db: Session = Depends(get_db)
):
    """
    Filter strings using natural language queries.
    
    Example: "all single word palindromic strings"
    """
    try:
        # Parse natural language into filters
        parsed_filters = parse_natural_language_query(query)
        
        if not parsed_filters:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to parse natural language query"
            )
        
        # Apply filters
        strings = get_all_strings_with_filters(db=db, **parsed_filters)
        
        # Format response
        data = [
            StringAnalysisResponse(
                id=s.id,
                value=s.value,
                properties=StringProperties(
                    length=s.length,
                    is_palindrome=s.is_palindrome,
                    unique_characters=s.unique_characters,
                    word_count=s.word_count,
                    sha256_hash=s.sha256_hash,
                    character_frequency_map=s.character_frequency_map
                ),
                created_at=s.created_at
            )
            for s in strings
        ]
        
        return NaturalLanguageResponse(
            data=data,
            count=len(data),
            interpreted_query={
                "original": query,
                "parsed_filters": parsed_filters
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Query parsed but resulted in conflicting filters: {str(e)}"
        )


@app.delete("/strings/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_string(string_value: str, db: Session = Depends(get_db)):
    """
    Delete a string by its value.
    
    Returns 204 on success, 404 if not found.
    """
    deleted = delete_string_by_value(db, string_value)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    return None


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"\n🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'SQLite'}")
    print(f"📚 Docs: http://127.0.0.1:{settings.PORT}/docs\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"\n👋 {settings.APP_NAME} shutting down...\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )