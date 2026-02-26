"""
==============================================================
ADDING IMAGES TO PDF USING PyMuPDF
==============================================================

Topics Covered:
    1. Insert Image
    2. Resize Image
    3. Positioning Image
    4. Add Watermark (Center Transparent)
    5. Add Logo (Top Right Corner)

Author: ANUJ
"""

# 1. Import Library
import fitz    # PyMuPDF


# 2. File Configuration
input_pdf = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/Searching_Text.pdf"
image_path = "./input/logo_bg_remove.png"   # Use PNG/JPG


# 3. Open PDF
doc = fitz.open(input_pdf)


# # ============================================================
# # EXAMPLE 1: INSERT IMAGE AT FIXED POSITION
# # ============================================================
# for page in doc:
    
#     # Define rectangle (x0, y0, x1, y1)
#     # Here placing image at top-left corner
#     rect = fitz.Rect(20, 20, 150, 100)

#     page.insert_image(rect, filename = image_path)
 
# print("✅ Example 1: Image inserted at fixed position.")


# # ============================================================
# # EXAMPLE 2: RESIZE IMAGE PROPERLY
# # ============================================================
# for page in doc:

#     # Desired width & height
#     width = 400
#     height = 200

#     x0, y0 = 200, 150
#     x1, y1 = x0 + width, y0 + height

#     rect = fitz.Rect(x0, y0, x1, y1)

#     page.insert_image(rect, filename=image_path)

# print("✅ Example 2: Image resized and inserted.")


# # ============================================================
# # EXAMPLE 3: POSITION IMAGE TOP-RIGHT (Dynamic Positioning)
# # ============================================================
# for page in doc:

#     page_width = page.rect.width

#     img_width = 120
#     img_height = 60

#     # Right margin = 20
#     x1 = page_width - 20
#     x0 = x1 - img_width

#     y0 = 20
#     y1 = y0 + img_height

#     rect = fitz.Rect(x0, y0, x1, y1)

#     page.insert_image(rect, filename=image_path)

# print("✅ Example 3: Logo placed top-right dynamically.")


# ============================================================
# EXAMPLE 4: ADD WATERMARK (CENTERED)
# ============================================================
for page in doc:

    page_width = page.rect.width
    page_height = page.rect.height

    watermark_width = 300
    watermark_height = 200

    # Center calculation
    x0 = (page_width - watermark_width) / 2
    y0 = (page_height - watermark_height) / 2
    x1 = x0 + watermark_width
    y1 = y0 + watermark_height

    rect = fitz.Rect(x0, y0, x1, y1)

    page.insert_image(
        rect,
        filename=image_path,
        overlay=False  # Put behind text
    )

print("✅ Example 4: Watermark added to center.")


# ------------------------------------------------------------
# 4️⃣ Save Document
# ------------------------------------------------------------
doc.save(output_path)
doc.close()

print("🎯 All image operations completed successfully.")
