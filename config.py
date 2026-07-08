"""
config.py
---------
Centralized configuration for the News Reader CLI application.

Responsibilities:
    - Load environment variables from a `.env` file.
    - Expose application-wide constants (API base URL, categories, countries).
    - Validate that required configuration (API key) is present before the
      application starts, failing fast with a clear error message.

This module has no side effects on import other than loading environment
variables, so it is safe to import from anywhere in the project.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Final

from dotenv import load_dotenv

# Load variables from a local .env file into the process environment.
# If no .env file exists, this is a harmless no-op (real env vars still work).
load_dotenv()


class ConfigurationError(Exception):
    """Raised when required configuration (e.g. the API key) is missing or invalid."""


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

NEWS_API_BASE_URL: Final[str] = "https://newsapi.org/v2"

REQUEST_TIMEOUT_SECONDS: Final[int] = 10

DEFAULT_PAGE_SIZE: Final[int] = 10
MAX_PAGE_SIZE: Final[int] = 100

# Categories supported by the NewsAPI.org "top-headlines" endpoint.
VALID_CATEGORIES: Final[list[str]] = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]

# A curated subset of ISO 3166-1 alpha-2 country codes supported by NewsAPI.org,
# mapped to human-friendly display names for menus.
VALID_COUNTRIES: Final[dict[str, str]] = {
    "us": "United States",
    "gb": "United Kingdom",
    "ca": "Canada",
    "au": "Australia",
    "in": "India",
    "de": "Germany",
    "fr": "France",
    "it": "Italy",
    "jp": "Japan",
    "br": "Brazil",
    "mx": "Mexico",
    "za": "South Africa",
    "ae": "United Arab Emirates",
    "sg": "Singapore",
    "ie": "Ireland",
}

VALID_SORT_OPTIONS: Final[list[str]] = ["relevancy", "popularity", "publishedAt"]


@dataclass(frozen=True)
class Settings:
    """
    Immutable application settings, populated from environment variables.

    Attributes:
        api_key: The NewsAPI.org API key used to authenticate requests.
        default_country: Fallback country code for top-headlines requests.
        default_page_size: Fallback number of articles to request per call.
    """

    api_key: str
    default_country: str = "us"
    default_page_size: int = DEFAULT_PAGE_SIZE
    request_timeout: int = REQUEST_TIMEOUT_SECONDS
    base_url: str = NEWS_API_BASE_URL
    categories: list[str] = field(default_factory=lambda: list(VALID_CATEGORIES))
    countries: dict[str, str] = field(default_factory=lambda: dict(VALID_COUNTRIES))


def load_settings() -> Settings:
    """
    Load and validate application settings from environment variables.

    Returns:
        A populated, validated Settings instance.

    Raises:
        ConfigurationError: If the NEWS_API_KEY environment variable is
            missing, empty, or still set to the placeholder value from
            `.env.example`.
    """
    api_key = os.getenv("NEWS_API_KEY", "").strip()

    if not api_key:
        raise ConfigurationError(
            "NEWS_API_KEY is missing. Create a '.env' file (see '.env.example') "
            "and set NEWS_API_KEY=<your_api_key>. Get a free key at "
            "https://newsapi.org/register"
        )

    if api_key.lower() in {"your_api_key_here", "changeme", "xxxx"}:
        raise ConfigurationError(
            "NEWS_API_KEY is still set to a placeholder value. Replace it in "
            "your '.env' file with a real API key from https://newsapi.org/register"
        )

    default_country = os.getenv("NEWS_DEFAULT_COUNTRY", "us").strip().lower()
    if default_country not in VALID_COUNTRIES:
        default_country = "us"

    return Settings(api_key=api_key, default_country=default_country)
