# ==============================================================
# EXTRACT ALL EMBEDDED IMAGES FROM FIRST PAGE
# ==============================================================

import fitz
import os

# --------------------------------------------------------------
# STEP 1: Open PDF
# --------------------------------------------------------------
pdf_path = "./../pdf_data/ansible-for-devops.pdf"
doc = fitz.open(pdf_path)

# Select first page
page = doc[81]

# --------------------------------------------------------------
# STEP 2: Get Image List
# full=True gives more detailed info
# --------------------------------------------------------------
image_list = page.get_images(full=True)

print(f"Total images found: {len(image_list)}")

# Create output folder
os.makedirs("extracted_images", exist_ok=True)

# --------------------------------------------------------------
# STEP 3: Loop Through Images
# --------------------------------------------------------------
for img_index, img in enumerate(image_list):

    # img[0] is xref
    xref = img[0]

    print(f"\nProcessing Image {img_index + 1}")
    print(f"XREF: {xref}")

    # ----------------------------------------------------------
    # STEP 4: Extract Image Bytes Using XREF
    # ----------------------------------------------------------
    base_image = doc.extract_image(xref)

    image_bytes = base_image["image"]
    image_ext = base_image["ext"]  # png, jpeg, etc.

    # ----------------------------------------------------------
    # STEP 5: Save Image to Disk
    # ----------------------------------------------------------
    image_filename = f"output/image_{img_index + 1}.{image_ext}"

    with open(image_filename, "wb") as image_file:
        image_file.write(image_bytes)

    print(f"Saved: {image_filename}")

doc.close()
