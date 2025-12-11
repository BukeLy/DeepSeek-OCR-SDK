# Multi-OCR-SDK

A collection of Python SDKs for different OCR providers, each optimized for specific use cases.

## Overview

This repository contains separate SDK implementations for different OCR providers:

- **DeepSeek-OCR** (`deepseek_ocr/`) - Free OCR via SiliconFlow
- **Qwen-VL-OCR** (`qwen_ocr/`) - Enterprise OCR via Alibaba Cloud DashScope

Each SDK is independent and can be used separately, allowing you to choose the best provider for your specific needs.

## Quick Comparison

| Feature | DeepSeek-OCR | Qwen-VL-OCR |
|---------|--------------|-------------|
| **Provider** | SiliconFlow | Alibaba Cloud DashScope |
| **Cost** | Free tier available | Paid (pay-as-you-go) |
| **TPM Limits** | ~80,000 (L0) | Configurable (high) |
| **Concurrency** | Limited | High |
| **Best For** | Testing, low-volume | Production, high-volume |
| **Upgrade** | Contact provider | Flexible pricing tiers |

## Installation

```bash
# Install the package
pip install -e .
```

## Usage

### DeepSeek-OCR

```python
from deepseek_ocr import DeepSeekOCR

client = DeepSeekOCR(
    api_key="your_siliconflow_api_key",
    base_url="https://api.siliconflow.cn/v1/chat/completions",
    model_name="deepseek-ai/DeepSeek-OCR"
)

text = client.parse("document.pdf")
```

### Qwen-VL-OCR

```python
from qwen_ocr import QwenOCR

client = QwenOCR(
    api_key="your_alibaba_cloud_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    model_name="qwen-vl-ocr"
)

text = client.parse("document.pdf")
```

## Directory Structure

```
.
├── deepseek_ocr/          # DeepSeek-OCR SDK
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── enums.py
│   ├── exceptions.py
│   ├── batch.py
│   └── README.md
├── qwen_ocr/              # Qwen-VL-OCR SDK
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── enums.py
│   ├── exceptions.py
│   ├── batch.py
│   └── README.md
├── examples/              # DeepSeek-OCR examples
├── examples_qwen/         # Qwen-VL-OCR examples
├── tests/                 # DeepSeek-OCR tests
└── tests_qwen/            # Qwen-VL-OCR tests
```

## When to Use Which SDK

### Use DeepSeek-OCR When:
- ✅ Testing and development
- ✅ Low-volume processing
- ✅ Cost-sensitive projects
- ✅ Getting started with OCR

### Use Qwen-VL-OCR When:
- ✅ Production environments
- ✅ Large-scale batch processing
- ✅ High concurrency requirements
- ✅ Medical/legal document processing
- ✅ Need for higher TPM limits

## Documentation

- [DeepSeek-OCR Documentation](./deepseek_ocr/README.md) - For the original DeepSeek-OCR SDK
- [Qwen-VL-OCR Documentation](./qwen_ocr/README.md) - For the new Qwen-VL-OCR SDK

## Examples

Each SDK has its own examples directory:

- `examples/` - DeepSeek-OCR examples
- `examples_qwen/` - Qwen-VL-OCR examples

## Testing

Run tests for each SDK separately:

```bash
# Test DeepSeek-OCR
python -m pytest tests/ -v

# Test Qwen-VL-OCR
python -m pytest tests_qwen/ -v
```

## Configuration

Each SDK uses its own environment variables:

### DeepSeek-OCR
```bash
export DS_OCR_API_KEY="your_siliconflow_api_key"
export DS_OCR_BASE_URL="https://api.siliconflow.cn/v1/chat/completions"
export DS_OCR_MODEL="deepseek-ai/DeepSeek-OCR"
```

### Qwen-VL-OCR
```bash
export QWEN_OCR_API_KEY="your_alibaba_cloud_api_key"
export QWEN_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
export QWEN_OCR_MODEL="qwen-vl-ocr"
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

- DeepSeek AI for the DeepSeek-OCR model
- Alibaba Cloud for the Qwen-VL-OCR models
- Original SDK implementation by @BukeLy

## Support

For issues or questions:
1. Check the SDK-specific README files
2. Review the examples
3. Open an issue on GitHub
