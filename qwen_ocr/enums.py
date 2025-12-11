"""
Enumerations for Qwen-VL-OCR SDK.

This module defines the enumeration types used throughout the SDK.
"""

from enum import Enum


class OCRMode(Enum):
    """
    OCR processing modes for Qwen-VL-OCR API.

    Attributes:
        FAST: Fast mode that returns pure text output.
              Best for simple documents.
              
        STANDARD: Standard mode with layout detection.
                  Optimal for most use cases including complex tables.
                  
        DETAILED: Detailed mode with bounding boxes.
                  Use for precise layout analysis.

    Performance Guidelines:
        - Simple documents: Use FAST
        - Complex tables: Use STANDARD
        - Layout analysis needed: Use DETAILED
    """

    FAST = "fast"
    STANDARD = "standard"
    DETAILED = "detailed"

    def get_prompt(self) -> str:
        """
        Get the API prompt string for this mode.

        Returns:
            The prompt string to send to the Qwen-VL-OCR API.
        """
        prompts = {
            OCRMode.FAST: "OCR",
            OCRMode.STANDARD: "OCR with layout detection",
            OCRMode.DETAILED: "Detailed OCR with bounding boxes",
        }
        return prompts[self]

    def __str__(self) -> str:
        """String representation of the mode."""
        return self.value
