# -------------------------------
# 1️⃣ Import Library
# -------------------------------
import fitz  # PyMuPDF
import os

# -------------------------------
# 2️⃣ File Configuration
# -------------------------------
input_pdf = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/Curved_Rectangle.pdf"

keyword = "ISBN 978-0-9863934-3-3"
page_index = 1            # 0-based index
curve_percentage = 50     # value based on percentage Valuse Should NOT Alowed More then 50% | MAX = 50%

# Create output folder if not exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# -------------------------------
# 3️⃣ Open PDF
# -------------------------------
doc = fitz.open(input_pdf)

# Page safety check
if page_index >= len(doc):
    raise ValueError(f"PDF has only {len(doc)} pages.")

page = doc[page_index]

# -------------------------------
# 4️⃣ Search Keyword
# -------------------------------
matches = page.search_for(keyword)

if not matches:
    raise ValueError(f"Keyword '{keyword}' not found on page {page_index}")

rect = matches[0]   # first match

# -------------------------------
# 5️⃣ Add Padding (Optional)
# -------------------------------
padding = 5  # increase box size
rect = fitz.Rect(
    rect.x0 - padding,
    rect.y0 - padding,
    rect.x1 + padding,
    rect.y1 + padding
)

# rectangle width & height
w = rect.width
h = rect.height

# safe radius calculation
max_radius = min(w, h)

# Convert value in percentages
radius = curve_percentage / 100  # 90% of allowed size

print(f"radius = {radius}")

page.draw_rect(
    rect,
    color = (1, 0, 0),
    width = 2,
    radius = radius
)

print("✅ Rounded rectangle drawn successfully.")

# -------------------------------
# 7️⃣ Save & Close
# -------------------------------
doc.save(output_path)
doc.close()

print("🎯 PDF saved successfully.")
