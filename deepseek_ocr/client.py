"""
Core OCR client for DeepSeek OCR SDK.

This module provides the main client for interacting with the DeepSeek OCR API.
"""

import asyncio
import base64
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional, Union, List

import aiohttp
import fitz  # PyMuPDF，fitz（在 Python 中来自包 PyMuPDF）是 MuPDF 的 Python 绑定，用于读取、渲染和操作 PDF/电子文档（也支持 EPUB、CBZ、XPS 等），常用于把 PDF 页面渲染成图片、提取文字/图片/注释、操作页面等。
import requests

from .config import OCRConfig
from .enums import OCRMode
from .exceptions import APIError, FileProcessingError, TimeoutError

logger = logging.getLogger(__name__)


class DeepSeekOCR:
    """
    Client for DeepSeek OCR API.

    This client provides both synchronous and asynchronous methods for
    document OCR processing using the DeepSeek OCR API.



    Example:
        >>> # Synchronous usage
        >>> client = DeepSeekOCR(api_key="your_api_key")
        >>> result = client.parse("document.pdf")
        >>> print(result)

        >>> # Asynchronous usage
        >>> import asyncio
        >>> async def main():
        ...     client = DeepSeekOCR(api_key="your_api_key")
        ...     result = await client.parse_async("document.pdf")
        ...     print(result)
        >>> asyncio.run(main())

    Attributes:
        config: OCRConfig instance containing all configuration.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: Optional[int] = None,
        max_tokens: Optional[int] = None,
        dpi: Optional[int] = None,
        **kwargs: str,

        # prompt 应该增加一个prompt参数，官方给出的几个promt确实不错，但应该给用户自定的选择
        #    OCRMode.FREE_OCR: "Free OCR.",
        #    OCRMode.GROUNDING: "<|grounding|>Convert the document to markdown.",
        #    OCRMode.OCR_IMAGE: "<|grounding|>OCR this image.",
    ):
        """
        Initialize DeepSeekOCR client.

        Args:
            api_key: API key for authentication. If not provided, will read
                     from DS_OCR_API_KEY environment variable.
            base_url: Base URL for the API endpoint.
            model_name: Name of the OCR model to use.
            timeout: Request timeout in seconds.
            max_tokens: Maximum tokens in response.
            dpi: DPI for PDF to image conversion (150, 200, or 300).
            **kwargs: Additional configuration parameters.

        Raises:
            ConfigurationError: If required configuration is missing or invalid.
        """
        # Build overrides dict from provided arguments
        overrides = {}
        if api_key is not None:
            overrides["api_key"] = api_key
        if base_url is not None:
            overrides["base_url"] = base_url
        if model_name is not None:
            overrides["model_name"] = model_name
        if timeout is not None:
            overrides["timeout"] = str(timeout)
        if max_tokens is not None:
            overrides["max_tokens"] = str(max_tokens)
        if dpi is not None:
            overrides["dpi"] = str(dpi)
        overrides.update(kwargs)

        self.config = OCRConfig.from_env(**overrides)
        logger.info(
            f"Initialized DeepSeekOCR client with model: {self.config.model_name}"
        )

    def _build_prompt(self, mode: OCRMode) -> str:
        """
        Build the prompt for the API request.

        Args:
            mode: OCR mode to use.

        Returns:
            Prompt string.
        """
        return mode.get_prompt()


    def _pdf_to_base64s(self, file_path: Union[str, Path], dpi: int) -> List[str]:
        """
        Convert all PDF pages to base64-encoded images.
        Returns a list of base64 image strings (one per page) in page order.

        Args:
            file_path: Path to the PDF file.
            dpi: DPI for rendering (150, 200, or 300).

        Returns:
            Base64-encoded image string.

        Raises:
            FileProcessingError: If file cannot be processed.
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileProcessingError(f"File not found: {file_path}")

            doc = fitz.open(str(file_path))
            if len(doc) == 0:
                raise FileProcessingError(f"PDF has no pages: {file_path}")

            b64_images: List[str] = []
            # Render every page
            for i in range(len(doc)):
                page = doc[i]
                matrix = fitz.Matrix(dpi / 72, dpi / 72)  #为什么是dpi/72？dpi不是设置150、200、300吗？是不是应该取公约数？
                pixel = page.get_pixmap(matrix=matrix)
                img_bytes = pixel.tobytes("png")
                b64_images.append(base64.b64encode(img_bytes).decode("utf-8"))

            doc.close()
            logger.debug(
                f"Converted PDF to images: {len(b64_images)} pages at {dpi} DPI" #为什么是dpi/72？dpi不是设置150、200、300吗？是不是应该取公约数？
            )
            return b64_images

        except Exception as e:
            raise FileProcessingError(f"Failed to process PDF: {e}") from e

    def _parse_api_result(self, result: Dict[str, Any]) -> str:
        """
        Parse the API result and return the cleaned text.
        Raises APIError if the result is invalid.
        """
        if "choices" not in result or len(result["choices"]) == 0:
            raise APIError("Invalid API response: no choices returned")

        text = result["choices"][0]["message"]["content"]
        return self._clean_output(text)

    def _clean_output(self, text: str) -> str:
        """
        Clean the OCR output by removing special tags.

        Args:
            text: Raw OCR output text.

        Returns:
            Cleaned text.
        """
        # Remove special tags but preserve HTML tables
        text = re.sub(r"<\|ref\|>", "", text)
        text = re.sub(r"<\|det\|>", "", text)
        return text.strip()

    async def _make_api_request_async(
        self, image_b64: str, prompt: str
    ) -> Dict[str, Any]:
        """
        Make async API request to DeepSeek OCR.

        Args:
            image_b64: Base64-encoded image.
            prompt: Prompt for OCR processing.

        Returns:
            API response as dictionary.

        Raises:
            APIError: If API returns an error.
            TimeoutError: If request times out.
        """
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "temperature": self.config.temperature,  #不知道有什么用，需要设置吗？
            "max_tokens": self.config.max_tokens,  #不知道有什么用，需要设置吗？
        }

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    self.config.base_url, headers=headers, json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise APIError(
                            f"API request failed: {error_text}",
                            status_code=response.status,
                            response_text=error_text,
                        )

                    result: Dict[str, Any] = await response.json()
                    return result

        except asyncio.TimeoutError as e:
            raise TimeoutError(
                f"Request timed out after {self.config.timeout} seconds"
            ) from e

    def _make_api_request_sync(self, image_b64: str, prompt: str) -> Dict[str, Any]:
        """
        Make synchronous API request to DeepSeek OCR.

        Args:
            image_b64: Base64-encoded image.
            prompt: Prompt for OCR processing.

        Returns:
            API response as dictionary.

        Raises:
            APIError: If API returns an error.
            TimeoutError: If request times out.
        """
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        try:
            response = requests.post(
                self.config.base_url,
                headers=headers,
                json=payload,
                timeout=self.config.timeout,
            )

            if response.status_code != 200:
                raise APIError(
                    f"API request failed: {response.text}",
                    status_code=response.status_code,
                    response_text=response.text,
                )

            result: Dict[str, Any] = response.json()
            return result

        except requests.Timeout as e:
            raise TimeoutError(
                f"Request timed out after {self.config.timeout} seconds"
            ) from e

    async def parse_async(
        self,
        file_path: Union[str, Path],
        mode: Union[str, OCRMode] = OCRMode.FREE_OCR,
        dpi: Optional[int] = None,
    ) -> str:
        """
        Parse document asynchronously.

        Args:
            file_path: Path to PDF or image file.
            mode: OCR mode ("free_ocr", "grounding", "ocr_image" or enum).
            dpi: DPI for PDF conversion. If None, uses config default.

        Returns:
            Extracted text in Markdown format.

        Raises:
            FileProcessingError: If file cannot be processed.
            APIError: If API returns an error.
            TimeoutError: If request times out.

        Example:
            >>> client = DeepSeekOCR(api_key="xxx")
            >>> text = await client.parse_async("document.pdf")
            >>> # With options
            >>> text = await client.parse_async(
            ...     "document.pdf",
            ...     mode="grounding",
            ...     dpi=300
            ... )
        """
        # Convert mode string to enum if needed
        if isinstance(mode, str):
            mode = OCRMode(mode)

        # Use config DPI if not specified
        if dpi is None:
            dpi = self.config.dpi

        # Convert PDF to base64
        logger.info(f"Processing {file_path} with mode={mode} and dpi={dpi}")
        multi_page_pdf_image_b64 = self._pdf_to_base64s(file_path, dpi)

        # Build prompt
        prompt = self._build_prompt(mode)

        # If single page
        if len(multi_page_pdf_image_b64) == 1:
            result = await self._make_api_request_async(multi_page_pdf_image_b64[0], prompt)
            text = self._parse_api_result(result)
            # Log token usage
            usage = result.get("usage", {})
            logger.debug(
                f"API usage: prompt_tokens={usage.get('prompt_tokens')}, "
                f"completion_tokens={usage.get('completion_tokens')}, "
                f"total_tokens={usage.get('total_tokens')}"
            )
        else:
            # if Multiple pages: make concurrent requests and combine outputs
            tasks = [self._make_api_request_async(img, prompt) for img in multi_page_pdf_image_b64]
            results = await asyncio.gather(*tasks)
            texts: List[str] = []
            total_prompt_tokens = 0
            total_completion_tokens = 0
            total_tokens = 0
            for idx, res in enumerate(results):
                page_text = self._parse_api_result(res)
                # Per-page fallback
                if (
                    self.config.fallback_enabled
                    and mode == OCRMode.FREE_OCR
                    and len(page_text) < self.config.min_output_threshold
                ):
                    logger.warning(
                        f"Page {idx+1} output too short ({len(page_text)} chars), falling back to {self.config.fallback_mode}"
                    )
                    fallback_prompt = self._build_prompt(
                        OCRMode(self.config.fallback_mode)
                    )
                    fallback_res = await self._make_api_request_async(multi_page_pdf_image_b64[idx], fallback_prompt)
                    page_text = self._parse_api_result(fallback_res)
                    # fallback usage
                    usage = fallback_res.get("usage", {})
                else:
                    usage = res.get("usage", {})

                total_prompt_tokens += int(usage.get("prompt_tokens", 0))
                total_completion_tokens += int(usage.get("completion_tokens", 0))
                total_tokens += int(usage.get("total_tokens", 0))
                texts.append(page_text)

            text = "\n\n".join(texts)
            logger.debug(
                f"API usage (aggregated): prompt_tokens={total_prompt_tokens}, "
                f"completion_tokens={total_completion_tokens}, total_tokens={total_tokens}"
            )

        # Note: single-page usage already logged; aggregated usage logged above for multi-page

        # Intelligent fallback (for single-page results handled here)
        if (
            self.config.fallback_enabled
            and mode == OCRMode.FREE_OCR
            and len(text) < self.config.min_output_threshold
        ):
            logger.warning(
                f"Output too short ({len(text)} chars), "
                f"falling back to {self.config.fallback_mode}"
            )
            return await self.parse_async(
                file_path,
                mode=OCRMode(self.config.fallback_mode),
                dpi=dpi,
            )

        logger.info(f"Successfully processed {file_path}: {len(text)} chars")
        return text

    def parse(
        self,
        file_path: Union[str, Path],
        mode: Union[str, OCRMode] = OCRMode.FREE_OCR,
        dpi: Optional[int] = None,
    ) -> str:
        """
        Parse document synchronously.

        Args:
            file_path: Path to PDF or image file.
            mode: OCR mode ("free_ocr", "grounding", "ocr_image" or enum).
            dpi: DPI for PDF conversion. If None, uses config default.

        Returns:
            Extracted text in Markdown format.

        Raises:
            FileProcessingError: If file cannot be processed.
            APIError: If API returns an error.
            TimeoutError: If request times out.

        Example:
            >>> client = DeepSeekOCR(api_key="xxx")
            >>> text = client.parse("document.pdf")
            >>> # With options
            >>> text = client.parse(
            ...     "document.pdf",
            ...     mode="grounding",
            ...     dpi=300
            ... )
        """
        # Convert mode string to enum if needed
        if isinstance(mode, str):
            mode = OCRMode(mode)

        # Use config DPI if not specified
        if dpi is None:
            dpi = self.config.dpi

        # Convert PDF to base64
        logger.info(f"Processing {file_path} with mode={mode} and dpi={dpi}")
        images_b64 = self._pdf_to_base64s(file_path, dpi)

        # Build prompt
        prompt = self._build_prompt(mode)

        # If single page, keep old behavior
        if len(images_b64) == 1:
            result = self._make_api_request_sync(images_b64[0], prompt)
            text = self._parse_api_result(result)
            usage = result.get("usage", {})
            logger.debug(
                f"API usage: prompt_tokens={usage.get('prompt_tokens')}, "
                f"completion_tokens={usage.get('completion_tokens')}, "
                f"total_tokens={usage.get('total_tokens')}"
            )
        else:
            texts: List[str] = []
            total_prompt_tokens = 0
            total_completion_tokens = 0
            total_tokens = 0
            for idx, img in enumerate(images_b64):
                result = self._make_api_request_sync(img, prompt)
                page_text = self._parse_api_result(result)
                # Per-page fallback for sync
                if (
                    self.config.fallback_enabled
                    and mode == OCRMode.FREE_OCR
                    and len(page_text) < self.config.min_output_threshold
                ):
                    logger.warning(
                        f"Page {idx+1} output too short ({len(page_text)} chars), falling back to {self.config.fallback_mode}"
                    )
                    fallback_prompt = self._build_prompt(OCRMode(self.config.fallback_mode))
                    fallback_result = self._make_api_request_sync(img, fallback_prompt)
                    page_text = self._parse_api_result(fallback_result)
                    usage = fallback_result.get("usage", {})
                else:
                    usage = result.get("usage", {})

                total_prompt_tokens += int(usage.get("prompt_tokens", 0))
                total_completion_tokens += int(usage.get("completion_tokens", 0))
                total_tokens += int(usage.get("total_tokens", 0))
                texts.append(page_text)

            text = "\n\n".join(texts)
            logger.debug(
                f"API usage (aggregated): prompt_tokens={total_prompt_tokens}, "
                f"completion_tokens={total_completion_tokens}, total_tokens={total_tokens}"
            )

        # Log token usage
        usage = result.get("usage", {})
        logger.debug(
            f"API usage: prompt_tokens={usage.get('prompt_tokens')}, "
            f"completion_tokens={usage.get('completion_tokens')}, "
            f"total_tokens={usage.get('total_tokens')}"
        )

        # Intelligent fallback
        if (
            self.config.fallback_enabled
            and mode == OCRMode.FREE_OCR
            and len(text) < self.config.min_output_threshold
        ):
            logger.warning(
                f"Output too short ({len(text)} chars), "
                f"falling back to {self.config.fallback_mode}"
            )
            return self.parse(
                file_path,
                mode=OCRMode(self.config.fallback_mode),
                dpi=dpi,
            )

        logger.info(f"Successfully processed {file_path}: {len(text)} chars")
        return text
