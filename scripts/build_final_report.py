# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Tạo Báo cáo đồ án toàn văn định dạng Word (.docx) và PDF (.pdf).

Quy trình thực hiện:
  1. Đọc cây nội dung BLOCKS từ scripts/report/content.py.
  2. Tạo tài liệu Word reports/BAO_CAO_DO_AN_NLP_ITVIEC.docx (thông qua python-docx).
  3. Sử dụng Microsoft Word COM (nếu có sẵn trên Windows):
     - Cập nhật tự động toàn bộ trường động (Dynamic Fields) và Mục lục (TOC).
     - Xuất PDF chất lượng cao có đầy đủ bookmarks cây tiêu đề chương mục.
  4. Nếu Word COM không khả dụng, tự động fallback sang ReportLab để tạo PDF độc lập.
  5. Đồng bộ báo cáo hoàn chỉnh sang thư mục nộp bài của Nhóm 12.

Cách chạy:
    python scripts/build_final_report.py
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Đảm bảo console Windows in tiếng Việt UTF-8 không bị lỗi charmap
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from report.content import BLOCKS, META  # noqa: E402
from report.render import build_docx, build_pdf  # noqa: E402

OUT_DIR = REPO_ROOT / "reports"
STEM = "BAO_CAO_DO_AN_NLP_ITVIEC"
SUBMISSION_DIR = (
    REPO_ROOT.parent
    / "Nhóm 12 - Phân tích cảm xúc đánh giá trên ITViec"
    / "Nhóm 12 - Phân tích cảm xúc đánh giá trên ITViec - Báo cáo"
)


def export_pdf_via_word_com(docx_path: Path, pdf_path: Path) -> bool:
    """Cập nhật dynamic fields trong Word và xuất PDF có bookmark navigation."""
    try:
        import win32com.client as win32
    except ImportError:
        return False

    word = None
    doc = None
    try:
        word = win32.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # wdAlertsNone
        doc = word.Documents.Open(str(docx_path.resolve()))

        # Cập nhật mục lục và dynamic fields
        doc.Fields.Update()
        doc.Save()

        # Xuất PDF với bookmarks tiêu đề (wdExportCreateHeadingBookmarks = 1)
        # 17 = wdExportFormatPDF, 0 = wdExportOptimizeForPrint
        doc.ExportAsFixedFormat(
            OutputFileName=str(pdf_path.resolve()),
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,
            Range=0,
            CreateBookmarks=1,
            DocStructureTags=True,
            BitmapMissingFonts=True,
        )
        return True
    except Exception as exc:
        print(f"[warning] Word COM gặp lỗi ({exc}), chuyển sang ReportLab...")
        return False
    finally:
        if doc is not None:
            try:
                doc.Close(SaveChanges=False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass


def sync_to_submission_dir(docx_path: Path, pdf_path: Path) -> None:
    """Đồng bộ báo cáo mới nhất sang thư mục nộp bài chuẩn bị bảo vệ đồ án."""
    if not SUBMISSION_DIR.exists():
        return

    dst_docx = SUBMISSION_DIR / "Báo cáo đồ án.docx"
    dst_pdf = SUBMISSION_DIR / "Báo cáo đồ án.pdf"

    for src, dst in [(docx_path, dst_docx), (pdf_path, dst_pdf)]:
        copied = False
        for attempt in range(3):
            try:
                shutil.copy2(src, dst)
                copied = True
                break
            except PermissionError:
                import time
                time.sleep(1)
            except Exception as exc:
                print(f"[warning] Không thể copy {dst.name}: {exc}")
                break
        if copied:
            print(f"[sync] Đồng bộ thành công: {dst.name} ({dst.stat().st_size / 1024:.0f} KB)")
        else:
            print(f"[warning] Tệp {dst.name} đang được mở bởi ứng dụng khác. Vui lòng đóng ứng dụng để đồng bộ lại!")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    docx_path = OUT_DIR / f"{STEM}.docx"
    pdf_path = OUT_DIR / f"{STEM}.pdf"

    print("=" * 70)
    print("XÂY DỰNG BÁO CÁO TOÀN VĂN ĐỒ ÁN NLP - ITVIEC (NHÓM 12)")
    print("=" * 70)

    # 1. Tạo file Word (.docx)
    build_docx(BLOCKS, docx_path, META)
    print(f"[docx] {docx_path.relative_to(REPO_ROOT)} ({docx_path.stat().st_size / 1024:.0f} KB)")

    # 2. Tạo file PDF (.pdf)
    exported_via_word = export_pdf_via_word_com(docx_path, pdf_path)
    if exported_via_word:
        print(f"[pdf ] {pdf_path.relative_to(REPO_ROOT)} ({pdf_path.stat().st_size / 1024:.0f} KB) [Word COM + Bookmarks]")
    else:
        build_pdf(BLOCKS, pdf_path, META)
        print(f"[pdf ] {pdf_path.relative_to(REPO_ROOT)} ({pdf_path.stat().st_size / 1024:.0f} KB) [ReportLab]")

    # 3. Đồng bộ sang thư mục nộp bài ngoài repo
    sync_to_submission_dir(docx_path, pdf_path)
    print("=" * 70)
    print("[success] Quá trình hoàn tất thành công!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
