"""
utils.py
--------
Reusable helper functions used across the News Reader CLI:
    - Input validation for user-supplied keywords, categories, countries, etc.
    - Text formatting helpers (truncation, date formatting).
    - Small, dependency-light utilities that don't belong in the API layer.

Keeping these separate from `news_service.py` and `main.py` keeps each
module focused on a single responsibility.
"""

from __future__ import annotations

from datetime import datetime

from config import VALID_CATEGORIES, VALID_COUNTRIES, VALID_SORT_OPTIONS, MAX_PAGE_SIZE


class ValidationError(Exception):
    """Raised when user-provided input fails validation."""


def validate_keyword(keyword: str) -> str:
    """
    Validate and normalize a search keyword.

    Args:
        keyword: Raw user input.

    Returns:
        The trimmed keyword.

    Raises:
        ValidationError: If the keyword is empty or too short to be useful.
    """
    cleaned = (keyword or "").strip()
    if not cleaned:
        raise ValidationError("Search keyword cannot be empty.")
    if len(cleaned) < 2:
        raise ValidationError("Search keyword must be at least 2 characters long.")
    return cleaned


def validate_category(category: str) -> str:
    """
    Validate a news category against the supported list.

    Args:
        category: Raw user input (case-insensitive).

    Returns:
        The normalized (lowercase) category string.

    Raises:
        ValidationError: If the category is not supported.
    """
    cleaned = (category or "").strip().lower()
    if cleaned not in VALID_CATEGORIES:
        allowed = ", ".join(VALID_CATEGORIES)
        raise ValidationError(f"Invalid category '{category}'. Choose from: {allowed}")
    return cleaned


def validate_country(country: str) -> str:
    """
    Validate a country code against the supported list.

    Args:
        country: Raw user input (case-insensitive ISO 3166-1 alpha-2 code).

    Returns:
        The normalized (lowercase) country code.

    Raises:
        ValidationError: If the country code is not supported.
    """
    cleaned = (country or "").strip().lower()
    if cleaned not in VALID_COUNTRIES:
        allowed = ", ".join(f"{code} ({name})" for code, name in VALID_COUNTRIES.items())
        raise ValidationError(f"Invalid country code '{country}'. Choose from: {allowed}")
    return cleaned


def validate_sort_by(sort_by: str) -> str:
    """
    Validate a 'sort by' option used for the search endpoint.

    Args:
        sort_by: Raw user input.

    Returns:
        The normalized sort option.

    Raises:
        ValidationError: If the option is not supported.
    """
    cleaned = (sort_by or "").strip().lower()
    if cleaned not in VALID_SORT_OPTIONS:
        allowed = ", ".join(VALID_SORT_OPTIONS)
        raise ValidationError(f"Invalid sort option '{sort_by}'. Choose from: {allowed}")
    return cleaned


def validate_page_size(page_size: int | str) -> int:
    """
    Validate the requested number of articles per page.

    Args:
        page_size: Raw user input, either an int or a numeric string.

    Returns:
        A valid integer page size between 1 and MAX_PAGE_SIZE.

    Raises:
        ValidationError: If the value is not a valid integer or out of range.
    """
    try:
        value = int(page_size)
    except (TypeError, ValueError):
        raise ValidationError(f"Page size must be a whole number, got '{page_size}'.") from None

    if not (1 <= value <= MAX_PAGE_SIZE):
        raise ValidationError(f"Page size must be between 1 and {MAX_PAGE_SIZE}.")
    return value


def format_published_date(raw_date: str | None) -> str:
    """
    Convert an ISO-8601 timestamp (as returned by NewsAPI.org) into a
    human-readable date/time string.

    Args:
        raw_date: ISO-8601 string, e.g. '2026-07-08T14:23:00Z'. May be None.

    Returns:
        A friendly string such as 'Jul 08, 2026 - 14:23 UTC', or
        'Unknown date' if parsing fails.
    """
    if not raw_date:
        return "Unknown date"
    try:
        normalized = raw_date.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
        return dt.strftime("%b %d, %Y - %H:%M UTC")
    except ValueError:
        return raw_date


def truncate_text(text: str | None, max_length: int = 200) -> str:
    """
    Truncate text to a maximum length, appending an ellipsis if shortened.

    Args:
        text: The text to truncate. May be None.
        max_length: Maximum number of characters to keep.

    Returns:
        The truncated (or original) text. Returns 'No description available.'
        if text is None or empty.
    """
    if not text:
        return "No description available."
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[: max_length].rstrip() + "..."


def safe_get(dictionary: dict, *keys: str, default: str = "N/A") -> str:
    """
    Safely retrieve a nested value from a dictionary, returning a default
    if any key is missing or the resulting value is None/empty.

    Args:
        dictionary: The dictionary to traverse.
        *keys: A sequence of keys to walk through, e.g. safe_get(article, "source", "name").
        default: Value to return if lookup fails.

    Returns:
        The resolved value, or the default.
    """
    current = dictionary
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    if current in (None, ""):
        return default
    return current
