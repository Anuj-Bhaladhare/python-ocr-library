from pdf2image import convert_from_path
import cv2
import pytesseract
import numpy as np


# # ==============================================================
# # => Practical Scenario #1: OCR on Scanned PDFs (Most Common) <=
# # ==============================================================
# # conversion of PDF -> to -> Images 
# images = convert_from_path(
#     "pdf_data/Unit-14.pdf",   # input PDF ka path
#     dpi = 300,                # DPI = image quality
#     thread_count = 4          # 4 CPU threads parallely used
# )

# # Save image as in PNG format in this purticular path
# for i, image in enumerate(images):
#     image.save(f"image_output/page_{i+1}.png", "PNG")


# # Extract text from Converted images by using PyTesseract library
# for page_no, img in enumerate(images, start = 1):
#     text = pytesseract.image_to_string(img)
#     print(f"--- Page {page_no} ---")
#     print(text)

# # ========================================================================
# # => 2️⃣ Practical Scenario #2: Invoice Layout Detection (Your Use Case) <=
# # ========================================================================
# """
#     PDF
#     ↓ pdf2image
#     Image
#     ↓ OpenCV (preprocessing)
#     ↓ OCR (layout data)
#     ↓ Block / paragraph detection
# """
# # --- Convert PDF to IMAGE ---
# images = convert_from_path(
#     "pdf_data/invoice.pdf",
#     dpi = 300,
#     thread_count = 4
# )

# # --- Save image in to machine ---
# for i, image in enumerate(images):
#     image.save(f"image_output/image_second_output_{i+1}.png", "PNG")

# # Apply Image PreProcessing opreration on image
# for img in images:
#     img_np = np.array(img)

#     # Convert image to Gray Scale
#     gray_image = cv2.cvtColor(
#         img_np,
#         cv2.COLOR_RGB2GRAY
#     )

#     # Convert image to Binarization image (0, 255)
#     _, thresh = cv2.threshold(
#         gray_image, 
#         180,
#         255,
#         cv2.THRESH_BINARY
#     )

#     # Show image in device
#     cv2.imshow("Invoice Page", thresh)
#     cv2.waitKey(0)    # wait until image tab is closed





# # ================================================================
# # =======> Example 3: Convert only one page (memory-safe) <=======
# # ================================================================
# images = convert_from_path(
#     "pdf_data/Unit-14.pdf",   # input PDF ka path
#     dpi = 300,                # Quality of page
#     first_page = 3,           # Start page
#     last_page = 3             # End page
# )

# # save page in to path
# images[0].save("image_output/convert_only_one_page.png")
