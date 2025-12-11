"""
Qwen-VL-OCR SDK

A simple and efficient Python SDK for Qwen-VL-OCR API (Alibaba Cloud DashScope).

Example:
    >>> from qwen_ocr import QwenOCR
    >>> client = QwenOCR(api_key="your_api_key")
    >>> text = client.parse("document.pdf")
    >>> print(text)

Features:
    - Simple and clean API
    - Three OCR modes: FAST, STANDARD, DETAILED
    - Intelligent fallback mechanism
    - Batch processing with progress tracking
    - Both sync and async support
    - Higher TPM limits compared to free alternatives
"""

from .batch import BatchProcessor, BatchResult, BatchSummary
from .client import QwenOCR
from .config import OCRConfig
from .enums import OCRMode
from .exceptions import (
    APIError,
    ConfigurationError,
    FileProcessingError,
    InvalidModeError,
    QwenOCRError,
    TimeoutError,
)

__version__ = "0.1.0"
__author__ = "Chengjie"
__license__ = "MIT"

__all__ = [
    # Main client
    "QwenOCR",
    # Configuration
    "OCRConfig",
    # Enums
    "OCRMode",
    # Batch processing
    "BatchProcessor",
    "BatchResult",
    "BatchSummary",
    # Exceptions
    "QwenOCRError",
    "ConfigurationError",
    "APIError",
    "FileProcessingError",
    "InvalidModeError",
    "TimeoutError",
    # Metadata
    "__version__",
]
