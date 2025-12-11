"""
Enumerations for DeepSeek OCR SDK.

This module defines the enumeration types used throughout the SDK.
"""

from enum import Enum


class OCRProvider(Enum):
    """
    OCR API provider types.
    
    Attributes:
        DEEPSEEK: DeepSeek-OCR models (e.g., deepseek-ai/DeepSeek-OCR)
        QWEN: Qwen-VL-OCR models (e.g., qwen-vl-ocr, qwen-vl-max-ocr)
    """
    
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    
    @classmethod
    def from_model_name(cls, model_name: str) -> "OCRProvider":
        """
        Detect provider from model name.
        
        Args:
            model_name: The model name string.
            
        Returns:
            OCRProvider enum value.
        """
        model_lower = model_name.lower()
        if "qwen" in model_lower:
            return cls.QWEN
        return cls.DEEPSEEK


class OCRMode(Enum):
    """
    OCR processing modes for OCR APIs.

    Attributes:
        FREE_OCR: Fast mode that returns pure Markdown output.
                  Best for 80% of document processing scenarios.
                  Speed: 3.95-10.95s per page (DeepSeek).

        GROUNDING: Advanced mode with HTML output and bounding boxes.
                   Optimal for complex tables (≥20 rows).
                   Speed: 5.18-8.31s per page (DeepSeek).

        OCR_IMAGE: Detailed mode with word-level bounding boxes.
                   Slower and less stable, use only for edge cases.
                   Speed: 19-26s per page (DeepSeek).

    Performance Guidelines:
        - Simple documents: Use FREE_OCR
        - Complex tables (≥20 rows): Use GROUNDING
        - Simple tables (<10 rows): Use FREE_OCR (not GROUNDING)
    """

    FREE_OCR = "free_ocr"
    GROUNDING = "grounding"
    OCR_IMAGE = "ocr_image"

    def get_prompt(self, provider: OCRProvider = OCRProvider.DEEPSEEK) -> str:
        """
        Get the API prompt string for this mode.

        Args:
            provider: The OCR provider to get prompt for.

        Returns:
            The prompt string to send to the OCR API.
        """
        if provider == OCRProvider.QWEN:
            # Qwen-VL-OCR uses simpler prompts
            qwen_prompts = {
                OCRMode.FREE_OCR: "OCR",
                OCRMode.GROUNDING: "OCR with layout detection",
                OCRMode.OCR_IMAGE: "Detailed OCR",
            }
            return qwen_prompts[self]
        else:
            # DeepSeek-OCR prompts
            deepseek_prompts = {
                OCRMode.FREE_OCR: "Free OCR.",
                OCRMode.GROUNDING: "<|grounding|>Convert the document to markdown.",
                OCRMode.OCR_IMAGE: "<|grounding|>OCR this image.",
            }
            return deepseek_prompts[self]

    def __str__(self) -> str:
        """String representation of the mode."""
        return self.value
