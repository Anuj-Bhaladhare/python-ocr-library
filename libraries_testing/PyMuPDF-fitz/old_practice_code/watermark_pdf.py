# Watermark PDF File using an Image

import fitz  # PyMuPDF

# Input PDF file
file_path = "./pdf_data/watermark-test.pdf"

# Watermark image file
image_path = "./pdf_data/watermark_logo.png"

# Open the PDF
pdf = fitz.open(file_path)

# Define watermark position (x0, y0, x1, y1)
# These values define a rectangle area on the page
rect = fitz.Rect(220, 220, 400, 400)

# Loop through all pages (watermark every page)
for page in pdf:
    page.insert_image(
        rect,                 # Position of image
        filename=image_path,  # Image file
        overlay=False         # False = behind text, True = above text
    )

# Save the new watermarked PDF
pdf.save("./output_data/pdf_file/watermark_pdf.pdf")

# Close the file
pdf.close()

print("Watermark added successfully!")
