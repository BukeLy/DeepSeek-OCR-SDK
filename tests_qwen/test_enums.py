"""Tests for enums module."""

from qwen_ocr import OCRMode


def test_ocr_mode_values():
    """Test OCR mode enum values."""
    assert OCRMode.FAST.value == "fast"
    assert OCRMode.STANDARD.value == "standard"
    assert OCRMode.DETAILED.value == "detailed"


def test_ocr_mode_prompts():
    """Test OCR mode prompt generation."""
    assert OCRMode.FAST.get_prompt() == "OCR"
    assert "layout" in OCRMode.STANDARD.get_prompt().lower()
    assert "bounding" in OCRMode.DETAILED.get_prompt().lower()


def test_ocr_mode_string_representation():
    """Test OCR mode string representation."""
    assert str(OCRMode.FAST) == "fast"
    assert str(OCRMode.STANDARD) == "standard"
    assert str(OCRMode.DETAILED) == "detailed"
