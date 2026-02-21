# # =======================================================================
# # ============ PART 1 — Compare 72 DPI vs 150 DPI vs 300 DPI ============
# # =======================================================================
# """ 
#      -----------------------------------------
#     | DPI | OCR Quality | File Size | Clarity |
#     | --- | ----------- | --------- | ------- |
#     | 72  | ❌ Poor     | Small     | Blurry  |
#     | 150 | ⚠ Medium    | Medium    | Better  |
#     | 300 | ✅ Best     | Large     | Sharp   |
#      -----------------------------------------

# """

# # ==============================================================
# # MULTI-DPI RENDERING DEMO
# # ==============================================================

# import fitz
# import cv2
# import numpy as np

# # --------------------------------------------------------------
# # STEP 1: Open PDF
# # --------------------------------------------------------------
# pdf_path = "./../pdf_data/ansible-for-devops.pdf"
# doc = fitz.open(pdf_path)

# # Select first page
# page = doc[15]

# # --------------------------------------------------------------
# # STEP 2: Function to Render Page at Custom DPI
# # --------------------------------------------------------------
# def render_page_at_dpi(page, dpi):
#     """
#     Render a PDF page at specific DPI
#     Returns OpenCV BGR image
#     """
#     zoom = dpi / 72  # 72 is default PDF DPI
#     matrix = fitz.Matrix(zoom, zoom)

#     # Render without alpha channel (faster, OCR friendly)
#     pix = page.get_pixmap(matrix=matrix, alpha=False)

#     # Convert to NumPy
#     img = np.frombuffer(pix.samples, dtype=np.uint8)
#     img = img.reshape(pix.height, pix.width, pix.n)

#     # Convert RGB -> BGR for OpenCV
#     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#     return img


# # --------------------------------------------------------------
# # STEP 3: Render at Different DPIs
# # --------------------------------------------------------------
# img_72  = render_page_at_dpi(page, 72)
# img_150 = render_page_at_dpi(page, 150)
# img_300 = render_page_at_dpi(page, 300)

# # --------------------------------------------------------------
# # STEP 4: Save Results
# # --------------------------------------------------------------
# cv2.imwrite("./output/invoice_72dpi.png", img_72)
# cv2.imwrite("./output/invoice_150dpi.png", img_150)
# cv2.imwrite("./output/invoice_300dpi.png", img_300)

# print("✅ Multi-DPI images saved.")

# doc.close()






# ========================================================================
# ============ PART 2 — Understanding RGBA vs RGB Practically ============
# ========================================================================
"""
    👉 PDF ko high-quality image me convert karta hai
    👉 Transparent background (alpha) ko remove karta hai
    👉 Image ko OpenCV compatible format me save karta hai
        - R → Red
        - G → Green
        - B → Blue
        - A → Alpha (Transparency)
"""

import fitz
import numpy as np
import cv2

doc = fitz.open("./../pdf_data/ansible-for-devops.pdf")
page = doc[15]

zoom = 300 / 72
matrix = fitz.Matrix(zoom, zoom)

# alpha=True -> RGBA
pix_rgba = page.get_pixmap(matrix=matrix, alpha=True)

# Convert to NumPy
img_rgba = np.frombuffer(pix_rgba.samples, dtype=np.uint8)
img_rgba = img_rgba.reshape(pix_rgba.height, pix_rgba.width, pix_rgba.n)

print("Channels:", pix_rgba.n)  # Should print 4

# Remove alpha manually
img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)

# Convert to BGR
img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

cv2.imwrite("./output/invoice_rgba_removed.png", img_bgr)

doc.close()



















