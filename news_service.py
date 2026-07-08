"""
news_service.py
----------------
Service layer responsible for all communication with the NewsAPI.org REST API.

Design notes:
    - This module knows nothing about the terminal UI (Rich) or user input
      parsing; it only knows how to talk to the API and return clean,
      validated Python data structures (or raise a NewsAPIError).
    - Keeping this separation means `main.py` could be swapped for a web
      backend or a different UI without touching this file at all.
"""

from __future__ import annotations

from typing import Any

import requests

from config import Settings


class NewsAPIError(Exception):
    """
    Raised for any failure while communicating with NewsAPI.org.

    This includes network failures, timeouts, non-200 HTTP responses, and
    API-level error payloads (e.g. invalid API key, rate limit exceeded).
    """


class NewsService:
    """
    Thin, well-behaved client for the NewsAPI.org 'everything' and
    'top-headlines' endpoints.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Args:
            settings: Application settings containing the API key, base URL,
                and request timeout.
        """
        self._settings = settings
        self._session = requests.Session()
        self._session.headers.update({"X-Api-Key": settings.api_key})

    def close(self) -> None:
        """Release the underlying HTTP session's resources."""
        self._session.close()

    def __enter__(self) -> "NewsService":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    # ------------------------------------------------------------------- #
    # Public API
    # ------------------------------------------------------------------- #

    def search_news(
        self,
        keyword: str,
        sort_by: str = "publishedAt",
        page_size: int = 10,
        language: str = "en",
    ) -> list[dict[str, Any]]:
        """
        Search all articles matching a keyword using the '/everything' endpoint.

        Args:
            keyword: The search query.
            sort_by: One of 'relevancy', 'popularity', 'publishedAt'.
            page_size: Number of results to request (1-100).
            language: ISO-639-1 language code to filter results.

        Returns:
            A list of article dictionaries as returned by the API.

        Raises:
            NewsAPIError: On any network, HTTP, or API-level error.
        """
        params = {
            "q": keyword,
            "sortBy": sort_by,
            "pageSize": page_size,
            "language": language,
        }
        payload = self._request("/everything", params)
        return payload.get("articles", [])

    def get_top_headlines(
        self,
        country: str = "us",
        category: str | None = None,
        page_size: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Fetch top headlines using the '/top-headlines' endpoint.

        Args:
            country: ISO 3166-1 alpha-2 country code.
            category: Optional category filter (e.g. 'technology').
            page_size: Number of results to request (1-100).

        Returns:
            A list of article dictionaries as returned by the API.

        Raises:
            NewsAPIError: On any network, HTTP, or API-level error.
        """
        params: dict[str, Any] = {"country": country, "pageSize": page_size}
        if category:
            params["category"] = category

        payload = self._request("/top-headlines", params)
        return payload.get("articles", [])

    # ------------------------------------------------------------------- #
    # Internal helpers
    # ------------------------------------------------------------------- #

    def _request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Perform a GET request against the NewsAPI.org API and validate the response.

        Args:
            endpoint: API path beginning with '/', e.g. '/top-headlines'.
            params: Query string parameters.

        Returns:
            The parsed JSON response body.

        Raises:
            NewsAPIError: Wraps network errors, timeouts, HTTP errors, and
                API-reported error statuses into a single, user-friendly
                exception type.
        """
        url = f"{self._settings.base_url}{endpoint}"

        try:
            response = self._session.get(
                url, params=params, timeout=self._settings.request_timeout
            )
        except requests.exceptions.Timeout as exc:
            raise NewsAPIError(
                "The request to NewsAPI.org timed out. Check your internet "
                "connection and try again."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise NewsAPIError(
                "Could not connect to NewsAPI.org. Check your internet "
                "connection and try again."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise NewsAPIError(f"An unexpected network error occurred: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise NewsAPIError(
                "Received an invalid (non-JSON) response from NewsAPI.org."
            ) from exc

        if response.status_code != 200 or data.get("status") == "error":
            message = data.get("message", "Unknown error returned by NewsAPI.org.")
            code = data.get("code", response.status_code)
            raise NewsAPIError(self._friendly_error(code, message))

        return data

    @staticmethod
    def _friendly_error(code: Any, message: str) -> str:
        """
        Translate common NewsAPI.org error codes into actionable, friendly
        messages for the end user.

        Args:
            code: The error code from the API (or HTTP status code).
            message: The raw error message from the API.

        Returns:
            A friendlier error string, falling back to the raw message.
        """
        friendly_map = {
            "apiKeyInvalid": "Your API key is invalid. Double-check NEWS_API_KEY in your .env file.",
            "apiKeyMissing": "No API key was sent. Ensure NEWS_API_KEY is set in your .env file.",
            "apiKeyExhausted": "Your API key has exhausted its daily request quota (free tier limit reached).",
            "rateLimited": "You are being rate-limited by NewsAPI.org. Please wait a moment and try again.",
            401: "Authentication failed. Double-check NEWS_API_KEY in your .env file.",
            429: "Too many requests sent to NewsAPI.org. Please wait a moment and try again.",
        }
        return friendly_map.get(code, message)
