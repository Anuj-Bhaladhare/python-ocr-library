"""
Working with Coordinates in PyMuPDF

This script demonstrates:

✔ Understanding Rect
✔ Using fitz.Rect
✔ Coordinate system (top-left origin)
✔ Scaling & DPI effect
✔ Drawing rectangles around words and blocks
"""

# ------------------------------------------------------------
# 1️⃣ Import Required Libraries
# ------------------------------------------------------------
import fitz
import os


# ------------------------------------------------------------
# 2️⃣ Initialize Paths
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "..", "pdf_data", "ansible-for-devops.pdf")
OUTPUT_FILE = os.path.join(BASE_DIR, "output_coordinates_demo.pdf")


# ------------------------------------------------------------
# 3️⃣ Open Document
# ------------------------------------------------------------
doc = fitz.open(INPUT_FILE)
page = doc[15]  # First page

print("\n========== PAGE GEOMETRY ==========")
print("Page Width:", page.rect.width)
print("Page Height:", page.rect.height)
print("Page Rect:", page.rect)
print("MediaBox:", page.mediabox)
print("CropBox:", page.cropbox)


# ------------------------------------------------------------
# 4️⃣ Understanding fitz.Rect
# ------------------------------------------------------------
"""
    Rect(x0, y0, x1, y1)

    x0, y0 → top-left
    x1, y1 → bottom-right
"""

sample_rect = fitz.Rect(50, 50, 300, 120)

print("\nSample Rect Coordinates:", sample_rect)
print("Width:", sample_rect.width)
print("Height:", sample_rect.height)

# Draw this rectangle on page
page.draw_rect(sample_rect, color=(1, 0, 0), width=2)


# ------------------------------------------------------------
# 5️⃣ Draw Rectangles Around TEXT BLOCKS
# ------------------------------------------------------------
print("\nDrawing rectangles around text blocks...")

blocks = page.get_text("blocks")

for block in blocks:
    x0, y0, x1, y1, text, block_no, block_type = block

    if block_type == 0:  # Only text blocks
        block_rect = fitz.Rect(x0, y0, x1, y1)

        # Draw green rectangle
        page.draw_rect(block_rect, color=(0, 1, 0), width=1)


# ------------------------------------------------------------
# 6️⃣ Draw Rectangles Around WORDS
# ------------------------------------------------------------
print("Drawing rectangles around words...")

words = page.get_text("words")

for word in words:
    x0, y0, x1, y1, word_text, block_no, line_no, word_no = word

    word_rect = fitz.Rect(x0, y0, x1, y1)

    # Draw blue rectangle
    page.draw_rect(word_rect, color=(0, 0, 1), width=0.5)


# ------------------------------------------------------------
# 7️⃣ Scaling & DPI Effect
# ------------------------------------------------------------
"""
Rendering page at different DPI affects image resolution,
but NOT internal PDF coordinate system.

Higher DPI = Higher resolution image
Coordinates remain same in PDF space.
"""

print("\n========== DPI DEMONSTRATION ==========")

zoom = 2  # 2x scaling (approx 144 DPI instead of 72)
matrix = fitz.Matrix(zoom, zoom)

pix = page.get_pixmap(matrix=matrix)
print("Rendered Image Size (scaled):", pix.width, "x", pix.height)

# Save scaled image preview
pix.save(os.path.join(BASE_DIR, "scaled_preview.png"))


# ------------------------------------------------------------
# 8️⃣ Save Modified PDF
# ------------------------------------------------------------
doc.save(OUTPUT_FILE)
doc.close()

print("\nOutput PDF saved at:", OUTPUT_FILE)
print("Scaled image preview saved as scaled_preview.png")
print("\nCoordinate practice completed successfully.")
