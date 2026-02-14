import fitz  # PyMuPDF
import pytesseract
from pytesseract import Output
import cv2
import numpy as np

file_path = "./pdf_data/orignal_bill_ifss.pdf"

# Open PDF
pdf_doc = fitz.open(file_path)

# Load First Page
pdf_page_1 = pdf_doc[0]

# Convert PDF page to image (300 DPI for better OCR)
pix = pdf_page_1.get_pixmap(dpi=300)

# Save image
pix.save("./output_data/image_file/ifss_orignal_bill.png")

# Convert to numpy array
image = np.frombuffer(pix.samples, dtype=np.uint8)
image = image.reshape(pix.height, pix.width, pix.n)

# ====================================================
# ==================: Pre-Process :===================
# ====================================================

# Convert to OpenCV BGR format
if pix.n == 4:
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
else:
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

original = image

# Convert Image to Gray-Scale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convert Image to Binary Image
_, thresh_image = cv2.threshold(
    gray_image,
    100,     # try 60, 80, 100
    255,
    cv2.THRESH_BINARY
)

# Remove Noise From Image
def noise_removal(gray_image):
    """
    OCR-safe noise removal:
    - Preserves text shape, thickness, and spacing
    - Removes only background noise and tiny speckles
    """

    # 1️⃣ Edge-preserving denoising (SAFE for text)
    denoised = cv2.fastNlMeansDenoising(
        gray_image,
        None,
        h=10,                  # noise strength (8–12 safe)
        templateWindowSize=7,
        searchWindowSize=21
    )

    # 2️⃣ Light adaptive threshold (text-safe)
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # 3️⃣ Remove only tiny isolated noise (no text damage)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary,
        connectivity=8
    )

    clean = np.zeros(binary.shape, dtype=np.uint8)

    MIN_AREA = 30  # keeps characters, removes dots/noise

    for i in range(1, num_labels):  # skip background
        if stats[i, cv2.CC_STAT_AREA] > MIN_AREA:
            clean[labels == i] = 255

    return clean

noise_rm_image = noise_removal(thresh_image)
# cv2.imwrite("./output_data/image_file/noise_rm_image.png", noise_rm_image)

image_ocr_data = pytesseract.image_to_data(
    noise_rm_image,
    output_type=Output.DICT,
    config = "--oem 3 --psm 6"
)

# STEP 1️⃣ OCR → WORDS
words = []
n = len(image_ocr_data["text"])

for i in range(n):
    if image_ocr_data["level"][i] == 5:  # WORD's
        word = image_ocr_data["text"][i].strip()
        if not word:
            continue

        x = image_ocr_data["left"][i]
        y = image_ocr_data["top"][i]
        w = image_ocr_data["width"][i]
        h = image_ocr_data["height"][i]

        words.append({
            "word": word,
            "bbox": [x, y, w, h]
        })

# ==============: Draw Bonding Box on PDF in Selected Text:==============
scale = 72 / 300  # Convert image coords back to PDF coords
word_flag = False

word_input = input("Enter Word You want to Draw Bonding Box (if available in PDF File): ")

for word in words:
    if word["word"] == word_input:
        word_flag = True
        x_position, y_position, w_position, h_position = word["bbox"]
        rect = fitz.Rect(
            x_position * scale, 
            y_position * scale, 
            (x_position + w_position) * scale, 
            (y_position + h_position) * scale
        )
        pdf_page_1.draw_rect(
            rect, 
            color=(0, 1, 0), 
            width=0.5   # Green Box
        )


if not word_flag:
    print("Your Word is NOT Available in PDF File")
else:
    print("Bonding Box Draw Successfully...!")


pdf_doc.save("./output_data/image_file/unreadable_bounding_box.pdf")




























# # ==============: Draw Bonding Box on PDF :==============
# scale = 72 / 300  # Convert image coords back to PDF coords
# for word in words:
#     x_position, y_position, w_position, h_position = word["bbox"]
#     rect = fitz.Rect(
#         x_position * scale, 
#         y_position * scale, 
#         (x_position + w_position) * scale, 
#         (y_position + h_position) * scale
#     )
#     pdf_page_1.draw_rect(
#         rect, 
#         color=(0, 1, 0), 
#         width=0.5   # Green Box
#     )
# pdf_doc.save("./output_data/image_file/unreadable_bounding_box.pdf")



# # ==============: Draw Bonding Box on Image File :==============
# for i, word in enumerate(words, 1):
#     x, y, w, h = word["bbox"]

#     cv2.rectangle(
#         original,
#         (x, y),
#         (x + w, y + h),
#         (0, 255, 0),
#         2
#     )

#     cv2.putText(
#         original,
#         f"BLOCK {i}",
#         (x, y - 6),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (0, 255, 0),
#         1
#     )

# cv2.imwrite("./output_data/image_file/bounding_box_image.png", original)

