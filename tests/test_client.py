"""
Tests for the DeepSeekOCR client.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from deepseek_ocr import DeepSeekOCR
from deepseek_ocr.exceptions import FileProcessingError


@pytest.fixture
def mock_pdf():
    """Create a mock PDF document with multiple pages."""
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 3  # 3 pages

    # Mock pages
    mock_pages = []
    for i in range(3):
        mock_page = MagicMock()
        mock_pixmap = MagicMock()
        mock_pixmap.tobytes.return_value = f"page{i}_image_bytes".encode()
        mock_page.get_pixmap.return_value = mock_pixmap
        mock_pages.append(mock_page)

    mock_doc.__getitem__.side_effect = lambda idx: mock_pages[idx]
    return mock_doc


def test_pdf_to_base64_all_pages(mock_pdf):
    """Test processing all pages of a PDF."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    with patch("fitz.open", return_value=mock_pdf):
        with patch("pathlib.Path.exists", return_value=True):
            # Process all pages (default)
            result = client._pdf_to_base64(Path("test.pdf"), dpi=200, pages=None)

            # Should return a list of 3 base64 strings
            assert isinstance(result, list)
            assert len(result) == 3


def test_pdf_to_base64_single_page(mock_pdf):
    """Test processing a single page of a PDF."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    with patch("fitz.open", return_value=mock_pdf):
        with patch("pathlib.Path.exists", return_value=True):
            # Process single page
            result = client._pdf_to_base64(Path("test.pdf"), dpi=200, pages=1)

            # Should return a single base64 string
            assert isinstance(result, str)


def test_pdf_to_base64_specific_pages(mock_pdf):
    """Test processing specific pages of a PDF."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    with patch("fitz.open", return_value=mock_pdf):
        with patch("pathlib.Path.exists", return_value=True):
            # Process pages 1 and 3
            result = client._pdf_to_base64(Path("test.pdf"), dpi=200, pages=[1, 3])

            # Should return a list of 2 base64 strings
            assert isinstance(result, list)
            assert len(result) == 2


def test_pdf_to_base64_page_out_of_range(mock_pdf):
    """Test error handling for page out of range."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    with patch("fitz.open", return_value=mock_pdf):
        with patch("pathlib.Path.exists", return_value=True):
            # Try to access page 5 (out of range)
            with pytest.raises(FileProcessingError) as exc_info:
                client._pdf_to_base64(Path("test.pdf"), dpi=200, pages=5)

            assert "out of range" in str(exc_info.value).lower()


def test_pdf_to_base64_file_not_found():
    """Test error handling for non-existent file."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileProcessingError) as exc_info:
            client._pdf_to_base64(Path("nonexistent.pdf"), dpi=200)

        assert "not found" in str(exc_info.value).lower()


def test_pdf_to_base64_empty_pdf():
    """Test error handling for PDF with no pages."""
    client = DeepSeekOCR(api_key="test_key", base_url="http://test.com")

    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 0

    with patch("fitz.open", return_value=mock_doc):
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(FileProcessingError) as exc_info:
                client._pdf_to_base64(Path("empty.pdf"), dpi=200)

            assert "no pages" in str(exc_info.value).lower()
