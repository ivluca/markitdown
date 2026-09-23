<div align="center">

# 📄 MarkItDown

[![Upstream](https://img.shields.io/badge/upstream-microsoft%2Fmarkitdown-blue?logo=github)](https://github.com/microsoft/markitdown)
[![PyPI](https://img.shields.io/pypi/v/markitdown.svg?color=green)](https://pypi.org/project/markitdown/)
[![Python](https://img.shields.io/badge/python-3.10--3.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Chuyển đổi file sang Markdown — tối ưu cho LLM & pipeline phân tích văn bản**

[Cài đặt](#-cài-đặt) · [Sử dụng](#-sử-dụng) · [Script tiện ích](#-script-tiện-ích) · [Cập nhật](#-cập-nhật-từ-repo-gốc)

</div>

---

## 🗂️ Định dạng hỗ trợ

| Loại | Định dạng |
|---|---|
| 📄 Tài liệu | PDF · Word (`.docx`) · PowerPoint (`.pptx`) · Excel (`.xlsx`, `.xls`) |
| 🌐 Web | HTML · YouTube URL |
| 🖼️ Media | Ảnh (EXIF + OCR) · Audio (EXIF + phiên âm) |
| 📦 Khác | CSV · JSON · XML · ZIP · EPubs |

---

## 📦 Cài đặt

### 1. Tạo môi trường ảo

```bash
python -m venv .venv

source .venv/bin/activate        # Bash / Zsh
source .venv/bin/activate.fish   # Fish shell
```

### 2. Cài package

```bash
# Tất cả định dạng
pip install 'markitdown[all]'

# Hoặc chỉ những định dạng cần dùng
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

<details>
<summary>📋 Xem toàn bộ tùy chọn</summary>

| Tùy chọn | Dùng cho |
|---|---|
| `[all]` | Tất cả định dạng |
| `[pdf]` | PDF |
| `[docx]` | Word |
| `[pptx]` | PowerPoint |
| `[xlsx]` / `[xls]` | Excel mới / cũ |
| `[outlook]` | Email Outlook |
| `[audio-transcription]` | Phiên âm audio (wav, mp3) |
| `[youtube-transcription]` | Phụ đề YouTube |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[az-content-understanding]` | Azure Content Understanding |

</details>

---

## 🚀 Sử dụng

### Command Line

```bash
# Lưu ra file
markitdown file.pdf -o output.md

# In ra màn hình
markitdown file.pdf

# Pipe
cat file.pdf | markitdown
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("file.pdf")
print(result.markdown)
```

> [!TIP]
> Dùng `convert_local()` thay vì `convert()` khi chỉ cần đọc file local — an toàn hơn trong môi trường server.

### Dùng với LLM (mô tả ảnh)

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("image.jpg")
print(result.markdown)
```

<details>
<summary>☁️ Azure Document Intelligence / Content Understanding</summary>

```bash
# Document Intelligence
export MARKITDOWN_DOCINTEL_ENDPOINT="<endpoint>"
markitdown file.pdf -o output.md -d

# Content Understanding
export MARKITDOWN_CU_ENDPOINT="<endpoint>"
markitdown file.pdf --use-cu
```

</details>

---

## 🛠️ Script tiện ích

> Repo này có thêm 2 script tùy chỉnh không có trong bản gốc.

### `markitdown.sh` — Chạy nhanh, không cần activate venv

```bash
./markitdown.sh file.pdf -o output.md    # PDF
./markitdown.sh file.docx -o output.md   # Word
./markitdown.sh file.xlsx                # Excel → in ra màn hình
./markitdown.sh file.pptx -o output.md  # PowerPoint
cat file.pdf | ./markitdown.sh           # Pipe
```

**Dùng từ mọi nơi:**

```bash
# Thêm alias vào ~/.bashrc hoặc ~/.config/fish/config.fish
alias markitdown='/home/ubuntu/Programs/markitdown/markitdown.sh'

# Hoặc tạo symlink
sudo ln -s /home/ubuntu/Programs/markitdown/markitdown.sh /usr/local/bin/markitdown
```

---

### `extract.py` — Trích xuất text + ảnh (giữ đúng vị trí)

> [!NOTE]
> MarkItDown **không giữ lại ảnh**. Script này kết hợp MarkItDown (text chất lượng cao) với PyMuPDF / python-pptx / openpyxl để trích xuất ảnh và nhúng đúng vị trí vào Markdown.

**Cài thêm 1 lần:**

```bash
pip install pymupdf
```

**Cách dùng:**

```bash
python extract.py file.pdf
python extract.py file.pptx
python extract.py file.xlsx
python extract.py file.pdf --out ket_qua/
```

**Kết quả:**

```
📁 file_output/
├── 📝 output.md        ← text + ảnh đúng vị trí
├── 🖼️  page1_img10.png
├── 🖼️  page1_img11.png
└── 🖼️  page2_img15.png
```

**Phân công xử lý:**

| Phần | Xử lý bởi |
|---|---|
| Text · Bảng · Heading · Bullet | MarkItDown |
| Trích xuất ảnh + vị trí | PyMuPDF / python-pptx / openpyxl |
| Ghép & xuất output | `extract.py` |

**Hỗ trợ:** `.pdf` · `.pptx` · `.xlsx` · `.xls`

---

## 🔒 Bảo mật

> [!WARNING]
> Không truyền input không tin cậy trực tiếp vào MarkItDown trong môi trường server.

- Dùng `convert_local()` nếu chỉ cần đọc file local
- Kiểm soát chặt đường dẫn và URI scheme khi deploy

---

## 🔄 Cập nhật từ repo gốc

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

> [!NOTE]
> Nếu có conflict ở `README.md` (do đã tùy chỉnh), giữ lại bản của bạn hoặc merge thủ công rồi commit lại.
