"""
Custom exceptions for Qwen-VL-OCR SDK.

This module defines all custom exception types used by the SDK.
"""

from typing import Optional


class QwenOCRError(Exception):
    """Base exception for all Qwen-VL-OCR SDK errors."""

    pass


class ConfigurationError(QwenOCRError):
    """Raised when there is a configuration error."""

    pass


class APIError(QwenOCRError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
    ):
        """
        Initialize APIError.

        Args:
            message: Error message.
            status_code: HTTP status code from the API.
            response_text: Raw response text from the API.
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class FileProcessingError(QwenOCRError):
    """Raised when there is an error processing the input file."""

    pass


class InvalidModeError(QwenOCRError):
    """Raised when an invalid OCR mode is specified."""

    pass


class TimeoutError(QwenOCRError):
    """Raised when an API request times out."""

    pass
