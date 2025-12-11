"""Tests for enums module."""

from deepseek_ocr import OCRMode, OCRProvider


def test_ocr_mode_values():
    """Test OCR mode enum values."""
    assert OCRMode.FREE_OCR.value == "free_ocr"
    assert OCRMode.GROUNDING.value == "grounding"
    assert OCRMode.OCR_IMAGE.value == "ocr_image"


def test_ocr_provider_values():
    """Test OCR provider enum values."""
    assert OCRProvider.DEEPSEEK.value == "deepseek"
    assert OCRProvider.QWEN.value == "qwen"


def test_ocr_provider_from_model_name():
    """Test provider detection from model name."""
    # DeepSeek models
    assert OCRProvider.from_model_name("deepseek-ai/DeepSeek-OCR") == OCRProvider.DEEPSEEK
    assert OCRProvider.from_model_name("DeepSeek-OCR") == OCRProvider.DEEPSEEK
    
    # Qwen models
    assert OCRProvider.from_model_name("qwen-vl-ocr") == OCRProvider.QWEN
    assert OCRProvider.from_model_name("qwen-vl-max-ocr") == OCRProvider.QWEN
    assert OCRProvider.from_model_name("Qwen-VL-Plus-OCR") == OCRProvider.QWEN
    
    # Unknown models default to DeepSeek
    assert OCRProvider.from_model_name("some-other-model") == OCRProvider.DEEPSEEK


def test_ocr_mode_prompts_deepseek():
    """Test OCR mode prompt generation for DeepSeek."""
    assert OCRMode.FREE_OCR.get_prompt(OCRProvider.DEEPSEEK) == "Free OCR."
    assert "grounding" in OCRMode.GROUNDING.get_prompt(OCRProvider.DEEPSEEK).lower()
    assert "grounding" in OCRMode.OCR_IMAGE.get_prompt(OCRProvider.DEEPSEEK).lower()


def test_ocr_mode_prompts_qwen():
    """Test OCR mode prompt generation for Qwen."""
    assert OCRMode.FREE_OCR.get_prompt(OCRProvider.QWEN) == "OCR"
    assert OCRMode.GROUNDING.get_prompt(OCRProvider.QWEN) == "OCR with layout detection"
    assert OCRMode.OCR_IMAGE.get_prompt(OCRProvider.QWEN) == "Detailed OCR"


def test_ocr_mode_prompts_default():
    """Test OCR mode prompt generation with default provider."""
    # Default should be DeepSeek
    assert OCRMode.FREE_OCR.get_prompt() == "Free OCR."


def test_ocr_mode_string_representation():
    """Test OCR mode string representation."""
    assert str(OCRMode.FREE_OCR) == "free_ocr"
    assert str(OCRMode.GROUNDING) == "grounding"
    assert str(OCRMode.OCR_IMAGE) == "ocr_image"
