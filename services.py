"""
Business logic for string analysis and natural language processing.
"""

import hashlib
import re
from typing import Dict, Optional
from collections import Counter
from sqlalchemy.orm import Session
from models import StringAnalysisDB


# ============= String Analysis Functions =============

def compute_sha256(text: str) -> str:
    """Compute SHA-256 hash of a string."""
    return hashlib.sha256(text.encode()).hexdigest()


def is_palindrome(text: str) -> bool:
    """Check if string is a palindrome (case-insensitive, ignores spaces)."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    return cleaned == cleaned[::-1]


def count_unique_characters(text: str) -> int:
    """Count distinct characters in string."""
    return len(set(text))


def count_words(text: str) -> int:
    """Count words separated by whitespace."""
    return len(text.split())


def character_frequency(text: str) -> Dict[str, int]:
    """Create character frequency map."""
    return dict(Counter(text))


def analyze_string(value: str) -> Dict:
    """
    Analyze a string and compute all properties.
    
    Returns dict with all computed properties.
    """
    sha256_hash = compute_sha256(value)
    
    return {
        "id": sha256_hash,
        "value": value,
        "length": len(value),
        "is_palindrome": is_palindrome(value),
        "unique_characters": count_unique_characters(value),
        "word_count": count_words(value),
        "sha256_hash": sha256_hash,
        "character_frequency_map": character_frequency(value)
    }


# ============= Database Operations =============

def create_string_analysis(db: Session, analysis_data: Dict) -> StringAnalysisDB:
    """Create a new string analysis record in database."""
    db_string = StringAnalysisDB(**analysis_data)
    db.add(db_string)
    db.commit()
    db.refresh(db_string)
    return db_string


def get_string_by_value(db: Session, value: str) -> Optional[StringAnalysisDB]:
    """Retrieve string by its value."""
    return db.query(StringAnalysisDB).filter(StringAnalysisDB.value == value).first()


def get_string_by_id(db: Session, string_id: str) -> Optional[StringAnalysisDB]:
    """Retrieve string by its ID (sha256 hash)."""
    return db.query(StringAnalysisDB).filter(StringAnalysisDB.id == string_id).first()


def delete_string_by_value(db: Session, value: str) -> bool:
    """Delete string by value. Returns True if deleted, False if not found."""
    db_string = get_string_by_value(db, value)
    if db_string:
        db.delete(db_string)
        db.commit()
        return True
    return False


def get_all_strings_with_filters(
    db: Session,
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None
) -> list:
    """Get all strings with optional filters."""
    query = db.query(StringAnalysisDB)
    
    if is_palindrome is not None:
        query = query.filter(StringAnalysisDB.is_palindrome == is_palindrome)
    
    if min_length is not None:
        query = query.filter(StringAnalysisDB.length >= min_length)
    
    if max_length is not None:
        query = query.filter(StringAnalysisDB.length <= max_length)
    
    if word_count is not None:
        query = query.filter(StringAnalysisDB.word_count == word_count)
    
    if contains_character is not None:
        query = query.filter(StringAnalysisDB.value.contains(contains_character))
    
    return query.all()


# ============= Natural Language Processing =============

def parse_natural_language_query(query: str) -> Dict:
    """
    Parse natural language query into filter parameters.
    
    Examples:
    - "all single word palindromic strings" -> {word_count: 1, is_palindrome: true}
    - "strings longer than 10 characters" -> {min_length: 11}
    - "strings containing the letter z" -> {contains_character: 'z'}
    """
    query_lower = query.lower()
    filters = {}
    
    # Check for palindrome
    if 'palindrome' in query_lower or 'palindromic' in query_lower:
        filters['is_palindrome'] = True
    
    # Check for word count
    if 'single word' in query_lower:
        filters['word_count'] = 1
    elif 'two word' in query_lower or '2 word' in query_lower:
        filters['word_count'] = 2
    
    # Check for length constraints
    length_pattern = r'longer than (\d+)'
    match = re.search(length_pattern, query_lower)
    if match:
        filters['min_length'] = int(match.group(1)) + 1
    
    shorter_pattern = r'shorter than (\d+)'
    match = re.search(shorter_pattern, query_lower)
    if match:
        filters['max_length'] = int(match.group(1)) - 1
    
    # Check for specific character
    contains_pattern = r'contain(?:s|ing)?\s+(?:the\s+)?(?:letter\s+)?([a-z])'
    match = re.search(contains_pattern, query_lower)
    if match:
        filters['contains_character'] = match.group(1)
    
    # Check for first vowel
    if 'first vowel' in query_lower:
        filters['contains_character'] = 'a'
    
    return filters