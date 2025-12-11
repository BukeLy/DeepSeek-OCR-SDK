# Qwen-OCR Support Documentation

## Overview

This document describes the Qwen-VL-OCR support added to the DeepSeek-OCR-SDK on the `Qwen-OCR-SDK` branch.

## Motivation

As described in the original issue:
- **Problem**: DeepSeek-OCR via SiliconFlow has low TPM (Tokens Per Minute) limits, especially problematic for medical document processing
- **Impact**: Processing large documents triggers rate limits easily (e.g., 1-2 pages per 60 seconds)
- **Solution**: Add support for Qwen-VL-OCR via Alibaba Cloud, which offers:
  - Higher TPM limits
  - Pay-as-you-go pricing for increased concurrency
  - More stable performance for large-scale processing

## Implementation

### Architecture Changes

The implementation follows a **minimal-change, provider-agnostic** architecture:

1. **OCRProvider Enum** (`deepseek_ocr/enums.py`):
   - New enum to distinguish between DeepSeek and Qwen providers
   - Auto-detection from model name
   ```python
   class OCRProvider(Enum):
       DEEPSEEK = "deepseek"
       QWEN = "qwen"
       
       @classmethod
       def from_model_name(cls, model_name: str) -> "OCRProvider":
           model_lower = model_name.lower()
           if "qwen" in model_lower:
               return cls.QWEN
           return cls.DEEPSEEK
   ```

2. **Provider-Aware Prompts** (`deepseek_ocr/enums.py`):
   - Updated `OCRMode.get_prompt()` to accept provider parameter
   - Different prompts for DeepSeek and Qwen models
   ```python
   def get_prompt(self, provider: OCRProvider = OCRProvider.DEEPSEEK) -> str:
       if provider == OCRProvider.QWEN:
           qwen_prompts = {
               OCRMode.FREE_OCR: "OCR",
               OCRMode.GROUNDING: "OCR with layout detection",
               OCRMode.OCR_IMAGE: "Detailed OCR",
           }
           return qwen_prompts[self]
       else:
           # DeepSeek prompts
           ...
   ```

3. **Configuration Auto-Detection** (`deepseek_ocr/config.py`):
   - OCRConfig now auto-detects provider from model name
   - Added provider field (auto-populated in `__post_init__`)
   ```python
   def __post_init__(self) -> None:
       self.provider = OCRProvider.from_model_name(self.model_name)
       ...
   ```

4. **Client Integration** (`deepseek_ocr/client.py`):
   - Updated `_build_prompt()` to use provider-aware prompts
   ```python
   def _build_prompt(self, mode: OCRMode) -> str:
       return mode.get_prompt(self.config.provider)
   ```

### Usage Examples

#### DeepSeek-OCR (SiliconFlow)
```python
from deepseek_ocr import DeepSeekOCR

client = DeepSeekOCR(
    api_key="your_siliconflow_api_key",
    base_url="https://api.siliconflow.cn/v1/chat/completions",
    model_name="deepseek-ai/DeepSeek-OCR"
)
text = client.parse("document.pdf")
```

#### Qwen-VL-OCR (Alibaba Cloud)
```python
from deepseek_ocr import DeepSeekOCR

client = DeepSeekOCR(
    api_key="your_alibaba_cloud_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    model_name="qwen-vl-ocr"  # or qwen-vl-max-ocr
)
text = client.parse("document.pdf")  # Same API!
```

### Available Models

**DeepSeek-OCR**:
- `deepseek-ai/DeepSeek-OCR`

**Qwen-VL-OCR**:
- `qwen-vl-ocr` - Standard model
- `qwen-vl-max-ocr` - Enhanced model for complex documents
- `qwen-vl-plus-ocr` - Balanced performance and cost

## Testing

All tests pass with 100% backward compatibility:
- ✅ 34 tests pass (including new provider-specific tests)
- ✅ Existing DeepSeek-OCR functionality unchanged
- ✅ New Qwen-OCR tests verify provider detection and prompt generation

Run tests:
```bash
python -m pytest tests/ -v
```

## Documentation Updates

- ✅ README.md updated with Qwen-OCR examples (English and Chinese)
- ✅ Provider selection guide added
- ✅ Configuration examples for both providers
- ✅ New example file: `examples/03_qwen_ocr_usage.py`

## Provider Comparison

| Feature | DeepSeek-OCR (SiliconFlow) | Qwen-VL-OCR (Alibaba Cloud) |
|---------|---------------------------|----------------------------|
| **Free Tier** | ✅ Available | ❌ Paid only |
| **TPM Limits** | Low (~80,000) | High (configurable) |
| **Concurrency** | Limited | High (pay-as-you-go) |
| **Best For** | Testing, low-volume | Production, high-volume |
| **Rate Limit Example** | 1-2 pages/60s | 60+ pages/60s (with proper limits) |
| **Upgrade Path** | Contact provider | Flexible pricing tiers |

## Migration Guide

Existing code requires **zero changes** to continue using DeepSeek-OCR:

```python
# Existing code - still works exactly the same
client = DeepSeekOCR(
    api_key="your_api_key",
    base_url="https://api.siliconflow.cn/v1/chat/completions"
)
text = client.parse("document.pdf")
```

To switch to Qwen-OCR, only change the initialization:

```python
# New code - switch to Qwen-OCR
client = DeepSeekOCR(
    api_key="your_alibaba_api_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    model_name="qwen-vl-ocr"
)
text = client.parse("document.pdf")  # Everything else stays the same!
```

## Environment Variables

**DeepSeek-OCR**:
```bash
export DS_OCR_API_KEY="your_siliconflow_api_key"
export DS_OCR_BASE_URL="https://api.siliconflow.cn/v1/chat/completions"
export DS_OCR_MODEL="deepseek-ai/DeepSeek-OCR"
```

**Qwen-VL-OCR**:
```bash
export DS_OCR_API_KEY="your_alibaba_cloud_api_key"
export DS_OCR_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
export DS_OCR_MODEL="qwen-vl-ocr"
export DS_OCR_MAX_TOKENS=8000  # Recommended for Qwen
```

## API References

- **Qwen-VL-OCR Documentation**: https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference
- **Alibaba Cloud DashScope**: https://dashscope.aliyuncs.com/
- **SiliconFlow API**: https://api.siliconflow.cn/

## Files Changed

1. `deepseek_ocr/enums.py` - Added OCRProvider enum and provider-aware prompts
2. `deepseek_ocr/config.py` - Added provider auto-detection
3. `deepseek_ocr/client.py` - Updated to use provider-aware prompts
4. `deepseek_ocr/__init__.py` - Exported OCRProvider
5. `README.md` - Added Qwen-OCR documentation
6. `examples/03_qwen_ocr_usage.py` - New comprehensive example
7. `tests/test_enums.py` - Added provider tests
8. `tests/test_config.py` - Added provider detection tests

## Future Enhancements

Potential improvements for future versions:
- Support for additional OCR providers
- Provider-specific configuration presets
- Performance benchmarking tools
- Cost estimation utilities

## License

This enhancement maintains the MIT license of the original project.

## Credits

- Original SDK: @BukeLy
- Qwen-OCR Support: Implemented based on user request in issue discussion
- Alibaba Cloud for Qwen-VL-OCR models
