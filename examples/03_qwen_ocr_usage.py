"""
Example: Using Qwen-OCR with the SDK

This example demonstrates how to use Qwen-VL-OCR models from Alibaba Cloud
for OCR tasks with higher concurrency limits compared to free DeepSeek-OCR.

Qwen-OCR models available:
- qwen-vl-ocr: Standard model for OCR tasks
- qwen-vl-max-ocr: Enhanced model for complex documents
- qwen-vl-plus-ocr: Balanced performance and cost

API Provider: Alibaba Cloud DashScope
Documentation: https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference
"""

import asyncio
from pathlib import Path

from deepseek_ocr import DeepSeekOCR, OCRProvider


def basic_qwen_usage():
    """Basic synchronous usage with Qwen-OCR."""
    print("=== Basic Qwen-OCR Usage ===\n")

    # Initialize client with Qwen model
    # Note: You need to set your Alibaba Cloud API key
    client = DeepSeekOCR(
        api_key="your_alibaba_cloud_api_key",  # Replace with your API key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-ocr",  # or "qwen-vl-max-ocr", "qwen-vl-plus-ocr"
    )

    # The SDK automatically detects the provider from the model name
    print(f"Provider: {client.config.provider}")
    print(f"Model: {client.config.model_name}\n")

    # Parse a document (replace with your file path)
    # text = client.parse("sample_document.pdf")
    # print(text)


def advanced_qwen_usage():
    """Advanced usage with different Qwen models and modes."""
    print("=== Advanced Qwen-OCR Usage ===\n")

    # Use qwen-vl-max-ocr for complex documents
    client = DeepSeekOCR(
        api_key="your_alibaba_cloud_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-max-ocr",  # Higher accuracy
        timeout=120,  # Longer timeout for complex documents
        max_tokens=8000,  # More tokens for longer documents
    )

    # Process with different modes
    # mode="free_ocr" for fast processing
    # text = client.parse("document.pdf", mode="free_ocr")

    # mode="grounding" for complex tables with layout detection
    # text = client.parse("complex_table.pdf", mode="grounding")

    # Custom DPI for better quality
    # text = client.parse("high_res_document.pdf", dpi=300)


async def async_qwen_usage():
    """Asynchronous usage for batch processing with Qwen-OCR."""
    print("=== Async Qwen-OCR Usage ===\n")

    client = DeepSeekOCR(
        api_key="your_alibaba_cloud_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-ocr",
    )

    # Process multiple documents concurrently
    # files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
    # tasks = [client.parse_async(file) for file in files]
    # results = await asyncio.gather(*tasks)

    # for file, text in zip(files, results):
    #     print(f"{file}: {len(text)} characters")


def comparison_deepseek_vs_qwen():
    """Compare DeepSeek-OCR and Qwen-OCR configurations."""
    print("=== DeepSeek vs Qwen Configuration ===\n")

    # DeepSeek-OCR (via SiliconFlow)
    deepseek_client = DeepSeekOCR(
        api_key="your_siliconflow_api_key",
        base_url="https://api.siliconflow.cn/v1/chat/completions",
        model_name="deepseek-ai/DeepSeek-OCR",
    )
    print(f"DeepSeek Provider: {deepseek_client.config.provider}")
    print(f"DeepSeek Model: {deepseek_client.config.model_name}\n")

    # Qwen-OCR (via Alibaba Cloud)
    qwen_client = DeepSeekOCR(
        api_key="your_alibaba_cloud_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-ocr",
    )
    print(f"Qwen Provider: {qwen_client.config.provider}")
    print(f"Qwen Model: {qwen_client.config.model_name}\n")

    # Same API, different providers
    # Both use the same parse() and parse_async() methods
    # The SDK automatically handles provider-specific prompts


def environment_variable_setup():
    """Example of using environment variables for Qwen-OCR."""
    print("=== Environment Variable Setup ===\n")

    # Set these environment variables before running:
    # export DS_OCR_API_KEY="your_alibaba_cloud_api_key"
    # export DS_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    # export DS_OCR_MODEL="qwen-vl-ocr"

    # Then simply initialize without parameters
    # client = DeepSeekOCR()
    # text = client.parse("document.pdf")

    print(
        """
    Environment variables for Qwen-OCR:
    
    export DS_OCR_API_KEY="your_alibaba_cloud_api_key"
    export DS_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    export DS_OCR_MODEL="qwen-vl-ocr"  # or qwen-vl-max-ocr, qwen-vl-plus-ocr
    export DS_OCR_TIMEOUT=120
    export DS_OCR_MAX_TOKENS=8000
    """
    )


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Qwen-OCR SDK Examples")
    print("=" * 60 + "\n")

    basic_qwen_usage()
    print("\n" + "-" * 60 + "\n")

    advanced_qwen_usage()
    print("\n" + "-" * 60 + "\n")

    comparison_deepseek_vs_qwen()
    print("\n" + "-" * 60 + "\n")

    environment_variable_setup()
    print("\n" + "-" * 60 + "\n")

    print(
        """
    Note: All examples require valid API keys to work.
    Replace 'your_alibaba_cloud_api_key' with your actual API key.
    
    For Alibaba Cloud API keys:
    1. Visit https://www.aliyun.com/
    2. Create an account or sign in
    3. Navigate to DashScope
    4. Generate an API key
    
    Benefits of Qwen-OCR:
    - Higher TPM (Tokens Per Minute) limits
    - Paid tiers available for increased concurrency
    - Stable and reliable service from Alibaba Cloud
    - Multiple model variants for different use cases
    """
    )


if __name__ == "__main__":
    main()

    # Uncomment to run async example
    # asyncio.run(async_qwen_usage())
