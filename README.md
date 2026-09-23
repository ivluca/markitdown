# MarkItDown

> Fork từ [microsoft/markitdown](https://github.com/microsoft/markitdown) — công cụ chuyển đổi file sang Markdown, tối ưu cho LLM và pipeline phân tích văn bản.

**Hỗ trợ:** PDF · Word · Excel · PowerPoint · Ảnh · Audio · HTML · CSV · JSON · XML · ZIP · YouTube · EPubs

---

## Cài đặt

```bash
# 1. Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate        # Bash/Zsh
source .venv/bin/activate.fish   # Fish shell

# 2. Cài đặt
pip install 'markitdown[all]'

# Hoặc chỉ một số định dạng
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

<details>
<summary>Tùy chọn cài đặt theo định dạng</summary>

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

</details>

---

## Sử dụng

### CLI

```bash
markitdown file.pdf -o output.md   # Lưu ra file
markitdown file.pdf                 # In ra màn hình
cat file.pdf | markitdown           # Pipe
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("file.pdf")
print(result.markdown)

# Chỉ đọc file local (an toàn hơn)
result = md.convert_local("file.pdf")

# Dùng với LLM để mô tả ảnh
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("image.jpg")
```

<details>
<summary>Azure Document Intelligence / Content Understanding</summary>

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

## Script tiện ích

### `markitdown.sh` — Chạy không cần activate venv

```bash
./markitdown.sh file.pdf -o output.md
./markitdown.sh file.docx -o output.md
./markitdown.sh file.xlsx
cat file.pdf | ./markitdown.sh
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

> MarkItDown không giữ lại ảnh. Script này kết hợp **MarkItDown** (text) + **PyMuPDF / python-pptx / openpyxl** (ảnh) để tạo Markdown có ảnh đúng vị trí.

```bash
pip install pymupdf   # cài thêm 1 lần

python extract.py file.pdf
python extract.py file.pptx
python extract.py file.xlsx
python extract.py file.pdf --out ket_qua/
```

**Kết quả:**

```
file_output/
├── output.md        ← text + link ảnh đúng vị trí
├── page1_img10.png
└── ...
```

**Hỗ trợ:** `.pdf` · `.pptx` · `.xlsx` · `.xls`

---

## Bảo mật

- **Không** truyền input không tin cậy vào MarkItDown
- Dùng `convert_local()` thay vì `convert()` nếu chỉ cần đọc file local

---

## Cập nhật từ repo gốc

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

> Nếu có conflict ở `README.md` (do đã tùy chỉnh), chọn giữ bản nào phù hợp rồi commit lại.
