"""Tests for exceptions module."""

from qwen_ocr import (
    APIError,
    ConfigurationError,
    QwenOCRError,
    FileProcessingError,
    TimeoutError,
)


def test_base_exception():
    """Test base exception."""
    error = QwenOCRError("test error")
    assert str(error) == "test error"
    assert isinstance(error, Exception)


def test_configuration_error():
    """Test configuration error."""
    error = ConfigurationError("config error")
    assert str(error) == "config error"
    assert isinstance(error, QwenOCRError)


def test_api_error_with_details():
    """Test API error with status code and response."""
    error = APIError("api failed", status_code=500, response_text="Internal error")
    assert str(error) == "api failed"
    assert error.status_code == 500
    assert error.response_text == "Internal error"


def test_file_processing_error():
    """Test file processing error."""
    error = FileProcessingError("invalid file")
    assert str(error) == "invalid file"
    assert isinstance(error, QwenOCRError)


def test_timeout_error():
    """Test timeout error."""
    error = TimeoutError("request timed out")
    assert str(error) == "request timed out"
    assert isinstance(error, QwenOCRError)
