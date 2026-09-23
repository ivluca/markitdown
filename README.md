# MarkItDown

Công cụ chuyển đổi file sang Markdown, tối ưu cho LLM và pipeline phân tích văn bản.

**Hỗ trợ:** PDF · Word · Excel · PowerPoint · Ảnh · Audio · HTML · CSV · JSON · XML · ZIP · YouTube · EPubs

---

## Cài đặt

```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate        # Bash/Zsh
source .venv/bin/activate.fish   # Fish shell

# Cài đặt
pip install 'markitdown[all]'

# Hoặc chỉ một số định dạng
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

**Tùy chọn cài đặt theo định dạng:**

| Tùy chọn | Định dạng |
|---|---|
| `[all]` | Tất cả |
| `[pdf]` | PDF |
| `[docx]` | Word |
| `[pptx]` | PowerPoint |
| `[xlsx]` / `[xls]` | Excel mới / cũ |
| `[outlook]` | Outlook |
| `[audio-transcription]` | Audio (wav, mp3) |
| `[youtube-transcription]` | Phụ đề YouTube |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[az-content-understanding]` | Azure Content Understanding |

---

## Sử dụng

### CLI

```bash
markitdown file.pdf -o output.md     # Lưu ra file
markitdown file.pdf                  # In ra màn hình
cat file.pdf | markitdown            # Pipe
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("file.pdf")
print(result.markdown)

# Chỉ đọc file local (an toàn hơn)
result = md.convert_local("file.pdf")
```

### Dùng với LLM để mô tả ảnh

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("image.jpg")
print(result.markdown)
```

### Azure Document Intelligence

```bash
export MARKITDOWN_DOCINTEL_ENDPOINT="<endpoint>"
markitdown file.pdf -o output.md -d
```

### Azure Content Understanding

```bash
export MARKITDOWN_CU_ENDPOINT="<endpoint>"
markitdown file.pdf --use-cu
```

---

## Script tiện ích

### `markitdown.sh` — Chạy không cần activate venv

```bash
./markitdown.sh file.pdf -o output.md    # PDF
./markitdown.sh file.docx -o output.md   # Word
./markitdown.sh file.xlsx                # Excel (in ra màn hình)
./markitdown.sh file.pptx -o output.md  # PowerPoint
cat file.pdf | ./markitdown.sh           # Pipe
```

**Dùng toàn cục:**

```bash
# Alias — thêm vào ~/.bashrc hoặc ~/.config/fish/config.fish
alias markitdown='/home/ubuntu/Programs/markitdown/markitdown.sh'

# Hoặc symlink
sudo ln -s /home/ubuntu/Programs/markitdown/markitdown.sh /usr/local/bin/markitdown
```

---

### `extract.py` — Trích xuất text + ảnh (giữ đúng vị trí)

> MarkItDown **không giữ lại ảnh**. Script này kết hợp MarkItDown (text chất lượng cao) với PyMuPDF / python-pptx / openpyxl (trích xuất ảnh) để tạo Markdown có ảnh đúng vị trí.

**Cài thêm dependency:**

```bash
pip install pymupdf
```

**Cách dùng:**

```bash
python extract.py file.pdf
python extract.py file.pptx
python extract.py file.xlsx
python extract.py file.pdf --out ket_qua/   # chỉ định thư mục output
```

**Kết quả:**

```
file_output/
├── output.md        ← text + link ảnh đúng vị trí
├── page1_img10.png
└── ...
```

| Phần | Xử lý bởi |
|---|---|
| Text, bảng, heading, bullet | MarkItDown |
| Trích xuất ảnh + vị trí | PyMuPDF / python-pptx / openpyxl |
| Ghép kết quả | extract.py |

**Hỗ trợ:** `.pdf` · `.pptx` · `.xlsx` · `.xls`

---

## Bảo mật

- **Không** truyền input không tin cậy trực tiếp vào MarkItDown
- Dùng `convert_local()` thay vì `convert()` nếu chỉ cần đọc file local
- Kiểm soát chặt đường dẫn file trong môi trường server
