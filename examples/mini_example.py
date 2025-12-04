from pathlib import Path
import os
from deepseek_ocr import DeepSeekOCR

API_KEY = os.getenv("DS_OCR_API_KEY", "your_api_key_here")

def main():
    client = DeepSeekOCR(api_key=API_KEY)

    # Robust, cross-platform path resolved relative to this example file
    sample_pdf = Path(__file__).resolve().parent / "sample_docs" / "DeepSeek_OCR_paper.pdf"

    if not sample_pdf.exists():
        print(f"Error: expected sample file at {sample_pdf} not found.")
        return

    print("Example 1: Processing simple document with FREE_OCR...")
    try:
        text = client.parse(str(sample_pdf), mode="free_ocr")
        print(f"Extracted text ({len(text)} chars):")
        print(text)
        print("\n" + "=" * 60 + "\n")
        # Save result to a markdown file next to this example
        out_path = Path(__file__).resolve().parent / "mini_usage_output.md"
        try:
            out_path.write_text(text, encoding="utf-8")
            print(f"Saved OCR output to: {out_path}")
        except Exception as w:
            print(f"Failed to write output file: {w}")
    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == "__main__":
    main()