# Qwen-VL-OCR SDK

A simple and efficient Python SDK for Qwen-VL-OCR API (Alibaba Cloud DashScope).

## Overview

This SDK provides a clean, production-ready interface for converting documents (PDF, images) to Markdown text using Qwen-VL-OCR models. It offers higher TPM limits and better scalability compared to free alternatives.

## Key Features

- **Simple API**: Clean and intuitive interface, minimal learning curve
- **Three OCR Modes**:
  - `FAST`: Quick processing for simple documents
  - `STANDARD`: Balanced mode with layout detection for most use cases
  - `DETAILED`: Advanced mode with bounding boxes for complex layouts
- **Intelligent Fallback**: Automatically switches modes for better quality
- **Batch Processing**: Process multiple documents efficiently with progress tracking
- **Async & Sync**: Full support for both asynchronous and synchronous workflows
- **High Concurrency**: Higher TPM limits suitable for production workloads

## Installation

```bash
# Install from parent directory
pip install -e .
```

## Quick Start

```python
from qwen_ocr import QwenOCR

# Initialize client
client = QwenOCR(
    api_key="your_alibaba_cloud_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    model_name="qwen-vl-ocr"
)

# Parse document
text = client.parse("document.pdf")
print(text)
```

## Available Models

- `qwen-vl-ocr` - Standard model for general OCR tasks
- `qwen-vl-max-ocr` - Enhanced model for complex documents and tables
- `qwen-vl-plus-ocr` - Balanced performance and cost

## Configuration

### Environment Variables

```bash
export QWEN_OCR_API_KEY="your_alibaba_cloud_api_key"
export QWEN_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
export QWEN_OCR_MODEL="qwen-vl-ocr"
export QWEN_OCR_TIMEOUT=120
export QWEN_OCR_MAX_TOKENS=8000
export QWEN_OCR_DPI=200
```

### Programmatic Configuration

```python
from qwen_ocr import QwenOCR

client = QwenOCR(
    api_key="your_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    model_name="qwen-vl-max-ocr",
    timeout=120,
    max_tokens=8000,
    dpi=300
)
```

## Usage Examples

### Basic Usage

```python
from qwen_ocr import QwenOCR

client = QwenOCR(
    api_key="your_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
)

# Simple document
text = client.parse("invoice.pdf", mode="fast")

# Complex table
text = client.parse("statement.pdf", mode="standard")

# Custom DPI
text = client.parse("document.pdf", dpi=300)
```

### Async Usage

```python
import asyncio
from qwen_ocr import QwenOCR

async def main():
    client = QwenOCR(
        api_key="your_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    )
    text = await client.parse_async("document.pdf")
    print(text)

asyncio.run(main())
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from qwen_ocr import QwenOCR, BatchProcessor

async def batch_example():
    client = QwenOCR(
        api_key="your_api_key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    )
    processor = BatchProcessor(client, max_concurrent=10)

    files = list(Path("docs").glob("*.pdf"))
    summary = await processor.process_batch(
        files,
        mode="standard",
        show_progress=True
    )

    summary.print_summary()

asyncio.run(batch_example())
```

## Mode Selection Guide

| Document Type | Recommended Mode | Reason |
|---------------|-----------------|---------|
| Simple text (invoice, letter) | `FAST` | Quick processing |
| Complex tables | `STANDARD` | Layout detection |
| Mixed content with layout | `DETAILED` | Bounding boxes |

## Benefits Over Free Alternatives

| Feature | Qwen-VL-OCR | Free Alternatives |
|---------|-------------|------------------|
| **TPM Limits** | High (configurable) | Low (~80,000) |
| **Concurrency** | High (pay-as-you-go) | Limited |
| **Reliability** | Enterprise-grade | Variable |
| **Rate Limits** | 60+ pages/minute | 1-2 pages/minute |
| **Cost** | Paid tiers | Free with limits |

## API Reference

For complete API documentation, see the [Alibaba Cloud Documentation](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference).

## License

This project is licensed under the MIT License.

## Getting API Keys

1. Visit [Alibaba Cloud](https://www.aliyun.com/)
2. Create an account or sign in
3. Navigate to DashScope
4. Generate an API key

## Support

For issues or questions:
- Check the examples in `examples_qwen/`
- Review the test cases in `tests_qwen/`
- Refer to [Alibaba Cloud Documentation](https://help.aliyun.com/zh/model-studio/)
