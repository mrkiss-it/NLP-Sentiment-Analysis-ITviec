#!/usr/bin/env python3
"""Sinh Báo cáo đồ án toàn văn (.docx và .pdf) từ scripts/report/content.py.

Chạy:  python scripts/build_final_report.py
Kết quả: reports/BAO_CAO_DO_AN_NLP_ITVIEC.docx và .pdf
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from report.content import BLOCKS, META  # noqa: E402
from report.render import build_docx, build_pdf  # noqa: E402

OUT_DIR = ROOT / "reports"
STEM = "BAO_CAO_DO_AN_NLP_ITVIEC"


def main() -> int:
    docx_path = build_docx(BLOCKS, OUT_DIR / f"{STEM}.docx", META)
    print(f"[docx] {docx_path.relative_to(ROOT)}  "
          f"({docx_path.stat().st_size / 1024:.0f} KB)")
    pdf_path = build_pdf(BLOCKS, OUT_DIR / f"{STEM}.pdf", META)
    print(f"[pdf ] {pdf_path.relative_to(ROOT)}  "
          f"({pdf_path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
