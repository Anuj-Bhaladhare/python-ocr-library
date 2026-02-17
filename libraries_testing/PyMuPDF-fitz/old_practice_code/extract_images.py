# Extract Images from PDF
import fitz  # PyMuPDF
import os

file_path = "./pdf_data/pdf_with_image.pdf"

# Open the PDF file
pdf = fitz.open(file_path)

image_count = 0  # Counter for extracted images

# Loop through all pages
for page_index in range(len(pdf)):
    page = pdf[page_index]

    # Get list of images on the page
    image_list = page.get_images(full=True)

    print(f"Page {page_index + 1} has {len(image_list)} images")

    # Loop through each image
    for img_index, img in enumerate(image_list):
        xref = img[0]  # XREF number of the image

        # Extract image bytes
        base_image = pdf.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]  # Image extension (png, jpeg, etc.)

        # Create output filename
        image_filename = f"./output_data/image_file/image_page{page_index + 1}_{img_index + 1}.{image_ext}"

        # Save image to file
        with open(image_filename, "wb") as image_file:
            image_file.write(image_bytes)

        image_count += 1

# Close PDF
pdf.close()

print(f"\nTotal {image_count} images extracted successfully!")
