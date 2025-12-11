"""
Example: Basic usage of Qwen-VL-OCR SDK

This example demonstrates how to use Qwen-VL-OCR models from Alibaba Cloud
for OCR tasks with higher concurrency limits.

Qwen-VL-OCR models available:
- qwen-vl-ocr: Standard model for OCR tasks
- qwen-vl-max-ocr: Enhanced model for complex documents
- qwen-vl-plus-ocr: Balanced performance and cost

API Provider: Alibaba Cloud DashScope
Documentation: https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference
"""

from qwen_ocr import QwenOCR


def basic_usage():
    """Basic synchronous usage with Qwen-VL-OCR."""
    print("=== Basic Qwen-VL-OCR Usage ===\n")

    # Initialize client with Qwen model
    # Note: You need to set your Alibaba Cloud API key
    client = QwenOCR(
        api_key="your_alibaba_cloud_api_key",  # Replace with your API key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-ocr",  # or "qwen-vl-max-ocr", "qwen-vl-plus-ocr"
    )

    print(f"Model: {client.config.model_name}")
    print(f"Base URL: {client.config.base_url}\n")

    # Parse a document (replace with your file path)
    # text = client.parse("sample_document.pdf")
    # print(text)


def advanced_usage():
    """Advanced usage with different Qwen models and modes."""
    print("=== Advanced Qwen-VL-OCR Usage ===\n")

    # Use qwen-vl-max-ocr for complex documents
    client = QwenOCR(
        api_key="your_alibaba_cloud_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        model_name="qwen-vl-max-ocr",  # Higher accuracy
        timeout=120,  # Longer timeout for complex documents
        max_tokens=8000,  # More tokens for longer documents
    )

    # Process with different modes
    # mode="fast" for fast processing
    # text = client.parse("document.pdf", mode="fast")

    # mode="standard" for complex tables with layout detection
    # text = client.parse("complex_table.pdf", mode="standard")

    # Custom DPI for better quality
    # text = client.parse("high_res_document.pdf", dpi=300)


def environment_variable_setup():
    """Example of using environment variables for Qwen-VL-OCR."""
    print("=== Environment Variable Setup ===\n")

    # Set these environment variables before running:
    # export QWEN_OCR_API_KEY="your_alibaba_cloud_api_key"
    # export QWEN_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    # export QWEN_OCR_MODEL="qwen-vl-ocr"

    # Then simply initialize without parameters
    # client = QwenOCR()
    # text = client.parse("document.pdf")

    print(
        """
    Environment variables for Qwen-VL-OCR:
    
    export QWEN_OCR_API_KEY="your_alibaba_cloud_api_key"
    export QWEN_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    export QWEN_OCR_MODEL="qwen-vl-ocr"  # or qwen-vl-max-ocr, qwen-vl-plus-ocr
    export QWEN_OCR_TIMEOUT=120
    export QWEN_OCR_MAX_TOKENS=8000
    """
    )


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Qwen-VL-OCR SDK Examples")
    print("=" * 60 + "\n")

    basic_usage()
    print("\n" + "-" * 60 + "\n")

    advanced_usage()
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
    
    Benefits of Qwen-VL-OCR:
    - Higher TPM (Tokens Per Minute) limits
    - Paid tiers available for increased concurrency
    - Stable and reliable service from Alibaba Cloud
    - Multiple model variants for different use cases
    """
    )


if __name__ == "__main__":
    main()
