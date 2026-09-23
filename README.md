<div align="center">

# 📄 MarkItDown

[![Upstream](https://img.shields.io/badge/upstream-microsoft%2Fmarkitdown-blue?logo=github)](https://github.com/microsoft/markitdown)
[![PyPI](https://img.shields.io/pypi/v/markitdown.svg?color=green)](https://pypi.org/project/markitdown/)
[![Python](https://img.shields.io/badge/python-3.10--3.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Convert files to Markdown — optimized for LLMs & text analysis pipelines**

[Installation](#-installation) · [Usage](#-usage) · [Custom Scripts](#️-custom-scripts) · [Update](#-update-from-upstream)

</div>

---

## 🗂️ Supported Formats

| Type | Formats |
|---|---|
| 📄 Documents | PDF · Word (`.docx`) · PowerPoint (`.pptx`) · Excel (`.xlsx`, `.xls`) |
| 🌐 Web | HTML · YouTube URLs |
| 🖼️ Media | Images (EXIF + OCR) · Audio (EXIF + transcription) |
| 📦 Other | CSV · JSON · XML · ZIP · EPubs |

---

## 📦 Installation

### 1. Create a virtual environment

```bash
python -m venv .venv

source .venv/bin/activate        # Bash / Zsh
source .venv/bin/activate.fish   # Fish shell
```

### 2. Install the package

```bash
# All formats
pip install 'markitdown[all]'

# Or only the formats you need
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

<details>
<summary>📋 View all optional dependencies</summary>

| Option | Format |
|---|---|
| `[all]` | All formats |
| `[pdf]` | PDF |
| `[docx]` | Word |
| `[pptx]` | PowerPoint |
| `[xlsx]` / `[xls]` | Excel (new / old) |
| `[outlook]` | Outlook email |
| `[audio-transcription]` | Audio transcription (wav, mp3) |
| `[youtube-transcription]` | YouTube captions |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[az-content-understanding]` | Azure Content Understanding |

</details>

---

## 🚀 Usage

### Command Line

```bash
# Save to file
markitdown file.pdf -o output.md

# Print to stdout
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
> Prefer `convert_local()` over `convert()` when only reading local files — safer in server environments.

### With LLM (image descriptions)

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

## 🛠️ Custom Scripts

> This fork includes 2 additional scripts not present in the original repo.

### `markitdown.sh` — Run without activating venv

```bash
./markitdown.sh file.pdf -o output.md    # PDF
./markitdown.sh file.docx -o output.md   # Word
./markitdown.sh file.xlsx                # Excel → stdout
./markitdown.sh file.pptx -o output.md  # PowerPoint
cat file.pdf | ./markitdown.sh           # Pipe
```

**Use globally from anywhere:**

```bash
# Add alias to ~/.bashrc or ~/.config/fish/config.fish
alias markitdown='/home/ubuntu/Programs/markitdown/markitdown.sh'

# Or create a symlink
sudo ln -s /home/ubuntu/Programs/markitdown/markitdown.sh /usr/local/bin/markitdown
```

---

### `extract.py` — Extract text + images (preserving position)

> [!NOTE]
> MarkItDown **does not preserve images**. This script combines MarkItDown (high-quality text) with PyMuPDF / python-pptx / openpyxl to extract images and embed them at the correct position in the Markdown output.

**Install once:**

```bash
pip install pymupdf
```

**Usage:**

```bash
python extract.py file.pdf
python extract.py file.pptx
python extract.py file.xlsx
python extract.py file.pdf --out output_dir/
```

**Output structure:**

```
📁 file_output/
├── 📝 output.md        ← text + images at correct positions
├── 🖼️  page1_img10.png
├── 🖼️  page1_img11.png
└── 🖼️  page2_img15.png
```

**How it works:**

| Part | Handled by |
|---|---|
| Text · Tables · Headings · Bullets | MarkItDown |
| Image extraction + positioning | PyMuPDF / python-pptx / openpyxl |
| Merging & output | `extract.py` |

**Supported formats:** `.pdf` · `.pptx` · `.xlsx` · `.xls`

---

## 🔒 Security

> [!WARNING]
> Do not pass untrusted input directly to MarkItDown in server or hosted environments.

- Use `convert_local()` instead of `convert()` when only reading local files
- Restrict file paths and URI schemes when deploying as a service

---

## 🔄 Update from Upstream

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

> [!NOTE]
> If there is a conflict in `README.md` (due to local customizations), keep your version or merge manually, then commit again.
