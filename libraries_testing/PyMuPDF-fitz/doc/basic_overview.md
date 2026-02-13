Perfect 👨‍🏫

From now on, I’ll act as your **PyMuPDF (fitz) specialist instructor** — not just basic usage, but **production-level understanding**, performance optimization, layout handling, OCR pipelines, invoice processing, and PDF internals.

Since you’re working on **OCR + invoice understanding systems**, PyMuPDF is a powerful tool for:

* Reading PDFs (text + layout + metadata)
* Extracting blocks / lines / words with coordinates
* Converting PDF pages to images
* Drawing bounding boxes
* Editing PDFs
* Embedding text/images
* Fast page rendering (much faster than many other libraries)

---

# 📘 First — Mental Model of PyMuPDF

PyMuPDF works like this:

```
Document → Page → Text / Images / Blocks / Words
```

### Core Objects:

* `fitz.open()` → opens document
* `doc[n]` → access page
* `page.get_text()` → extract text
* `page.get_text("blocks")` → layout blocks
* `page.get_pixmap()` → convert to image
* `page.insert_text()` → write text
* `page.draw_rect()` → draw bounding box

---

# 🔥 Step 1 — Basic PDF Reading (Correct Way)

```python
import fitz  # PyMuPDF

doc = fitz.open("invoice.pdf")

print("Total Pages:", len(doc))

page = doc[0]  # First page

text = page.get_text()
print(text)

doc.close()
```

### Important:

Never use old syntax like:

```python
page.getText()
```

It is deprecated. Always use:

```python
page.get_text()
```

---

# 🔥 Step 2 — Extract Structured Layout (VERY IMPORTANT FOR YOU)

Since you work on invoice block detection, this is critical.

### Get Blocks with Coordinates

```python
blocks = page.get_text("blocks")

for block in blocks:
    x0, y0, x1, y1, text, block_no, block_type = block
    print("Block:", text)
    print("Coordinates:", (x0, y0, x1, y1))
```

Each block contains:

```
(x0, y0, x1, y1, text, block_number, block_type)
```

This is MUCH better than Tesseract block detection for digital PDFs.

---

# 🔥 Step 3 — Extract Words (For Precise Layout Control)

```python
words = page.get_text("words")

for word in words:
    x0, y0, x1, y1, text, block_no, line_no, word_no = word
    print(text, (x0, y0, x1, y1))
```

This is extremely useful when:

* Finding invoice number
* Detecting amount fields
* Matching keywords with coordinates
* Creating your own block merging logic

---

# 🔥 Step 4 — Convert PDF Page to Image (For OCR Pipeline)

Since you’re building OCR systems:

```python
page = doc[0]

pix = page.get_pixmap(dpi=300)  # High resolution
pix.save("page_1.png")
```

For OpenCV pipeline:

```python
import numpy as np
import cv2

pix = page.get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

if pix.n == 4:
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

cv2.imwrite("page_cv2.png", img)
```

---

# 🔥 Step 5 — Draw Bounding Boxes (For Visualization)

```python
for block in blocks:
    rect = fitz.Rect(block[:4])
    page.draw_rect(rect, color=(1, 0, 0), width=2)

doc.save("output_with_boxes.pdf")
```

Red boxes will be drawn around text blocks.

---

# ⚡ Important for Invoice Projects

Anuj, since you’re building invoice OCR systems:

### Digital PDF → Use PyMuPDF directly

(No OCR needed)

### Scanned PDF →

1. Convert page to image using PyMuPDF
2. Run Tesseract / EasyOCR
3. Post-process blocks

This hybrid pipeline is production-grade.

---

# 🧠 Advanced Topic (We Will Cover Step-by-Step)

If you continue learning with me, I’ll teach you:

* Text extraction modes: `"text"`, `"blocks"`, `"words"`, `"dict"`, `"rawdict"`
* Reading fonts & styles
* Extracting tables
* Detecting headers/footers
* Merging blocks properly (important for invoices)
* Memory optimization for large PDFs
* Parallel page processing
* PDF editing at scale
* Building full invoice parser using PyMuPDF

---

Now tell me 👇

Do you want to start with:

1. 🔹 Beginner fundamentals
2. 🔹 Layout & block engineering (recommended for you)
3. 🔹 Image rendering + OCR pipeline
4. 🔹 Advanced production-level PDF engineering

I’ll teach you step-by-step like a real mentor.


