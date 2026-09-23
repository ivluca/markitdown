#!/usr/bin/env python3
"""
extract.py — Kết hợp MarkItDown (text) + PyMuPDF/python-pptx/openpyxl (ảnh)
Giữ nguyên vị trí ảnh trong file markdown output.

Cách dùng:
    python extract.py <file> [--out <output_dir>]

Ví dụ:
    python extract.py report.pdf
    python extract.py slides.pptx --out my_output
    python extract.py data.xlsx
"""

import argparse
import os
import re
import sys


# ─────────────────────────────────────────────
#  PDF
# ─────────────────────────────────────────────
def extract_pdf(filepath: str, output_dir: str) -> str:
    try:
        import fitz
    except ImportError:
        print("❌ Thiếu thư viện: pip install pymupdf")
        sys.exit(1)

    try:
        from markitdown import MarkItDown
    except ImportError:
        print("❌ Thiếu thư viện: pip install markitdown")
        sys.exit(1)

    doc = fitz.open(filepath)

    # Bước 1: MarkItDown chuyển đổi toàn bộ text
    md_tool = MarkItDown()
    md_text = md_tool.convert(filepath).markdown

    # Bước 2: Tách markdown theo trang (nếu có dấu phân trang)
    # MarkItDown thường không đánh dấu trang → ta tự build theo trang
    pages_md: dict[int, str] = {}
    for page_num, page in enumerate(doc, 1):
        page_text = page.get_text("markdown").strip()
        pages_md[page_num] = page_text

    # Bước 3: Với mỗi trang, thu thập ảnh + ghép vào đúng vị trí
    final_md = f"<!-- Nguồn: {os.path.basename(filepath)} -->\n\n"

    for page_num, page in enumerate(doc, 1):
        final_md += f"\n---\n## 📄 Trang {page_num}\n\n"

        # Lấy blocks theo thứ tự từ trên xuống
        blocks = page.get_text("blocks", sort=True)

        for block in blocks:
            kind = block[6]

            if kind == 0:  # text
                text = block[4].strip()
                if text:
                    final_md += text + "\n\n"

            elif kind == 1:  # image
                xref = block[7] if len(block) > 7 else None
                if xref:
                    try:
                        pix = fitz.Pixmap(doc, xref)
                        if pix.n > 4:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_name = f"page{page_num}_img{xref}.png"
                        pix.save(os.path.join(output_dir, img_name))
                        final_md += f"![Hình trang {page_num}]({img_name})\n\n"
                    except Exception as e:
                        final_md += f"<!-- ảnh lỗi: {e} -->\n\n"

    return final_md


# ─────────────────────────────────────────────
#  PPTX
# ─────────────────────────────────────────────
def extract_pptx(filepath: str, output_dir: str) -> str:
    try:
        from pptx import Presentation
        from pptx.enum.shapes import MSO_SHAPE_TYPE
    except ImportError:
        print("❌ Thiếu thư viện: pip install python-pptx")
        sys.exit(1)

    try:
        from markitdown import MarkItDown
    except ImportError:
        print("❌ Thiếu thư viện: pip install markitdown")
        sys.exit(1)

    prs = Presentation(filepath)

    # Bước 1: MarkItDown lấy toàn bộ text (xử lý bảng, bullet tốt hơn)
    md_tool = MarkItDown()
    md_full = md_tool.convert(filepath).markdown

    # Tách markdown theo slide — MarkItDown dùng dấu "<!-- Slide X -->" hoặc "---"
    slide_texts = re.split(r"\n---+\n|<!-- [Ss]lide \d+ -->", md_full)
    slide_texts = [s.strip() for s in slide_texts if s.strip()]

    final_md = f"<!-- Nguồn: {os.path.basename(filepath)} -->\n\n"

    for slide_num, slide in enumerate(prs.slides, 1):
        final_md += f"\n---\n## 🖼️ Slide {slide_num}\n\n"

        # Text từ MarkItDown (chất lượng tốt hơn)
        if slide_num - 1 < len(slide_texts):
            final_md += slide_texts[slide_num - 1] + "\n\n"

        # Ảnh từ python-pptx (đúng vị trí)
        shapes_sorted = sorted(slide.shapes, key=lambda s: (s.top or 0, s.left or 0))
        for shape in shapes_sorted:
            if shape.shape_type == 13:  # PICTURE
                try:
                    img = shape.image
                    ext = img.ext or "png"
                    img_name = f"slide{slide_num}_shape{shape.shape_id}.{ext}"
                    with open(os.path.join(output_dir, img_name), "wb") as f:
                        f.write(img.blob)
                    final_md += f"![{shape.name}]({img_name})\n\n"
                except Exception as e:
                    final_md += f"<!-- ảnh lỗi: {e} -->\n\n"

    return final_md


# ─────────────────────────────────────────────
#  EXCEL
# ─────────────────────────────────────────────
def extract_excel(filepath: str, output_dir: str) -> str:
    try:
        from openpyxl import load_workbook
    except ImportError:
        print("❌ Thiếu thư viện: pip install openpyxl")
        sys.exit(1)

    try:
        from markitdown import MarkItDown
    except ImportError:
        print("❌ Thiếu thư viện: pip install markitdown")
        sys.exit(1)

    # Bước 1: MarkItDown chuyển bảng dữ liệu (xử lý tốt hơn)
    md_tool = MarkItDown()
    md_full = md_tool.convert(filepath).markdown

    # Tách theo sheet
    sheet_sections = re.split(r"\n## ", md_full)
    sheet_map: dict[str, str] = {}
    for section in sheet_sections:
        lines = section.strip().splitlines()
        if lines:
            sheet_name = lines[0].strip().rstrip(":")
            content = "\n".join(lines[1:]).strip()
            sheet_map[sheet_name] = content

    # Bước 2: openpyxl để lấy ảnh kèm vị trí anchor
    wb = load_workbook(filepath, data_only=True)
    final_md = f"<!-- Nguồn: {os.path.basename(filepath)} -->\n\n"

    for sheet in wb.worksheets:
        final_md += f"\n---\n## 📊 Sheet: {sheet.title}\n\n"

        # Lấy ảnh theo row anchor
        img_by_row: dict[int, list] = {}
        for img in sheet._images:
            try:
                row = img.anchor._from.row
            except Exception:
                row = -1
            img_by_row.setdefault(row, []).append(img)

        # Text từ MarkItDown
        matched_text = sheet_map.get(sheet.title, "")
        if not matched_text:
            # fallback: lấy theo thứ tự sheet
            idx = list(wb.sheetnames).index(sheet.title)
            values = list(sheet_map.values())
            matched_text = values[idx] if idx < len(values) else ""

        # Ghép text theo từng dòng + chèn ảnh đúng vị trí
        text_rows = matched_text.splitlines()
        for row_idx, row_text in enumerate(text_rows):
            # Chèn ảnh trước dòng này nếu anchor khớp
            for img in img_by_row.get(row_idx, []):
                try:
                    img_data = img._data()
                    img_name = f"{sheet.title}_img_row{row_idx}.png"
                    with open(os.path.join(output_dir, img_name), "wb") as f:
                        f.write(img_data)
                    final_md += f"![image]({img_name})\n\n"
                except Exception as e:
                    final_md += f"<!-- ảnh lỗi: {e} -->\n\n"

            if row_text.strip():
                final_md += row_text + "\n"

        # Ảnh không gắn với dòng nào
        for img in img_by_row.get(-1, []):
            try:
                img_data = img._data()
                img_name = f"{sheet.title}_img_extra.png"
                with open(os.path.join(output_dir, img_name), "wb") as f:
                    f.write(img_data)
                final_md += f"\n![image]({img_name})\n\n"
            except Exception:
                pass

    return final_md


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Trích xuất text (MarkItDown) + ảnh từ PDF/PPTX/Excel"
    )
    parser.add_argument("file", help="File đầu vào (.pdf, .pptx, .xlsx, .xls)")
    parser.add_argument("--out", default=None, help="Thư mục output (mặc định: <tên_file>_output)")
    args = parser.parse_args()

    filepath = args.file
    if not os.path.exists(filepath):
        print(f"❌ Không tìm thấy file: {filepath}")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = args.out or f"{base_name}_output"
    os.makedirs(output_dir, exist_ok=True)

    ext = os.path.splitext(filepath)[1].lower()
    print(f"📂 Output: {output_dir}/")

    if ext == ".pdf":
        print("📄 Đang xử lý PDF...")
        md = extract_pdf(filepath, output_dir)
    elif ext == ".pptx":
        print("🖼️  Đang xử lý PPTX...")
        md = extract_pptx(filepath, output_dir)
    elif ext in (".xlsx", ".xls"):
        print("📊 Đang xử lý Excel...")
        md = extract_excel(filepath, output_dir)
    else:
        print(f"❌ Định dạng chưa hỗ trợ: {ext}")
        print("   Hỗ trợ: .pdf | .pptx | .xlsx | .xls")
        sys.exit(1)

    md_path = os.path.join(output_dir, f"{base_name}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    img_count = len([f for f in os.listdir(output_dir) if f.endswith((".png", ".jpg", ".jpeg"))])
    print(f"✅ Xong!")
    print(f"   📝 Markdown : {md_path}")
    print(f"   🖼️  Ảnh      : {img_count} ảnh trong {output_dir}/")


if __name__ == "__main__":
    main()
