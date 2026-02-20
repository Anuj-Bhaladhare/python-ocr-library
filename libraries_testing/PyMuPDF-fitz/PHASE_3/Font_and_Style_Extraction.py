"""
Font & Style Extraction in PyMuPDF

This script demonstrates:

✔ Access span font
✔ Extract font size
✔ Detect bold / italic
✔ Extract color
✔ Automatically detect headings
"""

# ------------------------------------------------------------
# 1️⃣ Import Libraries
# ------------------------------------------------------------
import fitz
import os



# ---------------------------------------------------------
# 2. Initialize File Path
# ---------------------------------------------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/font-level-engineering.pdf"



# ------------------------------------------------------------
# 3️⃣ Open Document
# ------------------------------------------------------------
doc = fitz.open(file_path)
page = doc[15]  # First page for demo



# ------------------------------------------------------------
# 4️⃣ Extract Structured Layout
# ------------------------------------------------------------
layout = page.get_text("dict")

all_font_sizes = []

# Collect all font sizes for threshold calculation
for block in layout["blocks"]:
    if block["type"] != 0:
        continue

    for line in block["lines"]:
        for span in line["spans"]:
            all_font_sizes.append(span["size"])

# Determine heading threshold (bigger than average)
average_font_size = sum(all_font_sizes) / len(all_font_sizes)
heading_threshold = average_font_size + 2

print("Average Font Size:", average_font_size)
print("Heading Detection Threshold:", heading_threshold)



# ------------------------------------------------------------
# 5️⃣ Process Spans and Detect Headings
# ------------------------------------------------------------
print("\n========== FONT STYLE ANALYSIS ==========\n")

for block in layout["blocks"]:

    if block["type"] != 0:
        continue

    for line in block["lines"]:

        for span in line["spans"]:

            text = span["text"].strip()
            font_name = span["font"]
            font_size = span["size"]
            font_flags = span["flags"]
            font_color = span["color"]
            span_bbox = fitz.Rect(span["bbox"])

            if not text:
                continue

            # Detect bold / italic using bitwise
            is_bold = bool(font_flags & 16)
            is_italic = bool(font_flags & 2)

            print("Text:", text)
            print("Font:", font_name)
            print("Size:", font_size)
            print("Bold:", is_bold)
            print("Italic:", is_italic)
            print("Color:", font_color)
            print("-" * 40)

            # ------------------------------------------------
            # Heading Detection Logic
            # ------------------------------------------------
            if font_size > heading_threshold or is_bold:

                print(">>> Heading Detected:", text)

                # Draw rectangle around heading
                page.draw_rect(span_bbox, color=(1, 0, 0), width=2)



# ------------------------------------------------------------
# 6️⃣ Save Output
# ------------------------------------------------------------
doc.save(output_path)
doc.close()

print("\nHeading Detection Completed.")
print("Output saved at:", output_path)






